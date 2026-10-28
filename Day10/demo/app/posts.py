import math

from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for

from .auth import login_required
from .db import get_db
from .masking import current_keywords, mask_text

bp = Blueprint('posts', __name__)


def page_number():
    try:
        return max(1, int(request.values.get('page', '1')))
    except (ValueError, TypeError):
        return 1


def fetch_post(post_id, owner=False):
    post = get_db().execute('SELECT * FROM posts WHERE id=?', (post_id,)).fetchone()
    if post is None:
        abort(404)
    if owner and (g.user is None or post['author_id'] != g.user['id']):
        abort(403)
    return post


def validate_post():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    errors = {}
    if not 1 <= len(title) <= 200:
        errors['title'] = '제목은 1~200자로 입력해 주세요.'
    if not 1 <= len(content) <= 20000:
        errors['content'] = '내용은 1~20,000자로 입력해 주세요.'
    return title, content, errors


@bp.get('/')
def home():
    return redirect(url_for('posts.index'))


@bp.get('/posts')
def index():
    conn = get_db()
    count = conn.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    pages = max(1, math.ceil(count / 10))
    page = min(page_number(), pages)
    keywords = current_keywords()
    rows = conn.execute('SELECT id,title_raw FROM posts ORDER BY created_at DESC,id DESC LIMIT 10 OFFSET ?',
                        ((page - 1) * 10,)).fetchall()
    posts = [{'id': p['id'], 'title': mask_text(p['title_raw'], keywords)} for p in rows]
    return render_template('index.html', posts=posts, page=page, pages=pages)


@bp.route('/posts/new', methods=['GET', 'POST'])
@login_required
def create():
    errors = {}
    if request.method == 'POST':
        title, content, errors = validate_post()
        if not errors:
            conn = get_db()
            with conn:
                cursor = conn.execute('INSERT INTO posts(author_id,title_raw,content_raw) VALUES (?,?,?)',
                                      (g.user['id'], title, content))
            flash('새로운 이야기를 기록했어요.', 'success')
            return redirect(url_for('posts.detail', post_id=cursor.lastrowid), code=303)
    return render_template('editor.html', post=None, errors=errors, page=1), (400 if errors else 200)


def detail_response(post_id, error=None):
    row = fetch_post(post_id)
    keywords = current_keywords()
    post = {'id': row['id'], 'title': mask_text(row['title_raw'], keywords),
            'content': mask_text(row['content_raw'], keywords),
            'owned': g.user is not None and g.user['id'] == row['author_id']}
    comments = [{'nickname': r['nickname'], 'content': mask_text(r['content_raw'], keywords)} for r in
                get_db().execute('SELECT c.content_raw,u.nickname FROM comments c JOIN users u ON u.id=c.author_id '
                                 'WHERE c.post_id=? ORDER BY c.id', (post_id,))]
    return render_template('detail.html', post=post, comments=comments, error=error, page=page_number()), (400 if error else 200)


@bp.get('/posts/<int:post_id>')
def detail(post_id):
    return detail_response(post_id)


@bp.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = fetch_post(post_id, owner=True)
    errors = {}
    if request.method == 'POST':
        title, content, errors = validate_post()
        if not errors:
            conn = get_db()
            with conn:
                conn.execute('UPDATE posts SET title_raw=?,content_raw=?,updated_at=CURRENT_TIMESTAMP WHERE id=? AND author_id=?',
                             (title, content, post_id, g.user['id']))
            flash('이야기를 수정했어요.', 'success')
            return redirect(url_for('posts.detail', post_id=post_id, page=page_number()), code=303)
    return render_template('editor.html', post=post, errors=errors, page=page_number()), (400 if errors else 200)


@bp.post('/posts/<int:post_id>/delete')
@login_required
def delete(post_id):
    post = fetch_post(post_id, owner=True)
    if request.form.get('confirm') != 'yes':
        return render_template('delete.html', post_id=post_id, page=page_number())
    conn = get_db()
    with conn:
        conn.execute('DELETE FROM posts WHERE id=? AND author_id=?', (post_id, g.user['id']))
    flash('이야기를 삭제했어요.', 'info')
    return redirect(url_for('posts.index', page=page_number()), code=303)


@bp.post('/posts/<int:post_id>/comments')
@login_required
def comment(post_id):
    fetch_post(post_id)
    content = request.form.get('content', '').strip()
    if not 1 <= len(content) <= 2000:
        return detail_response(post_id, '댓글은 1~2,000자로 입력해 주세요.')
    conn = get_db()
    with conn:
        conn.execute('INSERT INTO comments(post_id,author_id,content_raw) VALUES (?,?,?)', (post_id, g.user['id'], content))
    flash('댓글을 남겼어요.', 'success')
    return redirect(url_for('posts.detail', post_id=post_id, page=page_number(), _anchor='comments'), code=303)
