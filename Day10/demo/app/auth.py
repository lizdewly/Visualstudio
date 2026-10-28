import hashlib
import re
import secrets
import sqlite3
import time
from functools import wraps

import click
from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db

bp = Blueprint('auth', __name__)


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def load_user():
    g.user = None
    token = session.get('token')
    if token:
        g.user = get_db().execute('SELECT u.id,u.email,u.nickname,u.role FROM sessions s JOIN users u ON u.id=s.user_id '
                                 'WHERE s.token_hash=? AND s.expires_at>?', (digest(token), int(time.time()))).fetchone()
        if g.user is None:
            session.clear()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            if request.method != 'GET':
                abort(403)
            flash('로그인하면 이야기를 남길 수 있어요.', 'info')
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None or g.user['role'] != 'ADMIN':
            abort(403)
        return view(*args, **kwargs)
    return wrapped


def validate_signup(email, nickname, password):
    errors = {}
    if len(email) > 254 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email):
        errors['email'] = '올바른 이메일 주소를 입력해 주세요.'
    if not 1 <= len(nickname) <= 30:
        errors['nickname'] = '닉네임은 1~30자로 입력해 주세요.'
    if not 8 <= len(password) <= 128 or not password.strip():
        errors['password'] = '비밀번호는 공백만 사용하지 않고 8~128자로 입력해 주세요.'
    return errors


def throttle(identity):
    """Bound hash workload without trusting proxy-controlled IP headers."""
    conn = get_db()
    now = int(time.time())
    buckets = [('identity:' + digest(identity), 10), ('ip:' + digest(request.remote_addr or 'unknown'), 60)]
    with conn:
        conn.execute('DELETE FROM auth_attempts WHERE window_start < ?', (now - 600,))
        for bucket, limit in buckets:
            row = conn.execute('SELECT attempts FROM auth_attempts WHERE bucket=?', (bucket,)).fetchone()
            if row and row['attempts'] >= limit:
                abort(429)
        for bucket, _ in buckets:
            conn.execute('INSERT INTO auth_attempts VALUES (?,1,?) ON CONFLICT(bucket) DO UPDATE SET attempts=attempts+1',
                         (bucket, now))


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if g.user:
        return redirect(url_for('posts.index'))
    errors = {}
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '')
        errors = validate_signup(email, nickname, password)
        if not errors:
            throttle(email)
            conn = get_db()
            try:
                with conn:
                    conn.execute('INSERT INTO users(email,nickname,password_hash) VALUES (?,?,?)',
                                 (email, nickname, generate_password_hash(password)))
                flash('가입이 완료됐어요. 로그인하고 첫 이야기를 남겨보세요.', 'success')
                return redirect(url_for('auth.login'), code=303)
            except sqlite3.IntegrityError:
                errors['email'] = '이미 가입된 이메일 주소예요.'
    return render_template('auth.html', signup=True, errors=errors), (400 if errors else 200)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('posts.index'))
    errors = {}
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if len(email) > 254 or not 8 <= len(password) <= 128:
            errors['form'] = '이메일 또는 비밀번호를 확인해 주세요.'
        else:
            throttle(email)
            conn = get_db()
            user = conn.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
            if user and check_password_hash(user['password_hash'], password):
                token = secrets.token_urlsafe(32)
                with conn:
                    conn.execute('DELETE FROM sessions WHERE expires_at <= ?', (int(time.time()),))
                    conn.execute('INSERT INTO sessions VALUES (?,?,?)',
                                 (digest(token), user['id'], int(time.time()) + current_app.config['SESSION_TTL']))
                session.clear()
                session['token'] = token
                flash('다시 만나 반가워요.', 'success')
                return redirect(url_for('posts.index'), code=303)
            errors['form'] = '이메일 또는 비밀번호를 확인해 주세요.'
    return render_template('auth.html', signup=False, errors=errors), (400 if errors else 200)


@bp.post('/logout')
@login_required
def logout():
    conn = get_db()
    with conn:
        conn.execute('DELETE FROM sessions WHERE token_hash=?', (digest(session['token']),))
    session.clear()
    flash('로그아웃했어요. 남긴 이야기는 그대로 보관됩니다.', 'info')
    return redirect(url_for('posts.index'), code=303)


@bp.cli.command('create-admin')
@click.option('--email', prompt=True)
@click.option('--nickname', prompt=True)
@click.password_option()
def create_admin(email, nickname, password):
    email, nickname = email.strip().lower(), nickname.strip()
    errors = validate_signup(email, nickname, password)
    if errors:
        raise click.ClickException(' '.join(errors.values()))
    conn = get_db()
    try:
        with conn:
            conn.execute("INSERT INTO users(email,nickname,password_hash,role) VALUES (?,?,?,'ADMIN')",
                         (email, nickname, generate_password_hash(password)))
    except sqlite3.IntegrityError as error:
        raise click.ClickException('이미 존재하는 이메일입니다. 기존 계정의 권한을 자동 변경하지 않습니다.') from error
    click.echo('관리자 생성 완료')
