import sqlite3

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from .auth import admin_required
from .db import get_db
from .masking import normalize_keyword

bp = Blueprint('admin', __name__)


@bp.route('/admin/masking', methods=['GET', 'POST'])
@admin_required
def masking():
    conn = get_db()
    error = None
    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        if not 1 <= len(keyword) <= 100:
            error = '키워드는 1~100자로 입력해 주세요.'
        elif conn.execute('SELECT COUNT(*) FROM masking_rules').fetchone()[0] >= 500:
            error = '규칙은 최대 500개까지 등록할 수 있어요.'
        else:
            try:
                with conn:
                    conn.execute('INSERT INTO masking_rules(keyword,normalized_keyword) VALUES (?,?)',
                                 (keyword, normalize_keyword(keyword)))
                flash('규칙을 추가했어요. 다음 조회부터 적용됩니다.', 'success')
                return redirect(url_for('admin.masking'), code=303)
            except sqlite3.IntegrityError:
                error = '이미 등록된 키워드예요.'
    rules = conn.execute('SELECT id,keyword FROM masking_rules ORDER BY id DESC').fetchall()
    return render_template('admin.html', rules=rules, error=error), (400 if error else 200)


@bp.post('/admin/masking/<int:rule_id>/delete')
@admin_required
def delete(rule_id):
    conn = get_db()
    with conn:
        cursor = conn.execute('DELETE FROM masking_rules WHERE id=?', (rule_id,))
    if cursor.rowcount == 0:
        abort(404)
    flash('규칙을 삭제했어요.', 'info')
    return redirect(url_for('admin.masking'), code=303)
