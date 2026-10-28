import json
import os
import sqlite3
from pathlib import Path

from flask import Flask, abort, render_template, request
from flask_wtf.csrf import CSRFProtect, CSRFError

csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=None, DATABASE_PATH=None, DEPLOYMENT=False,
        SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=False, MAX_CONTENT_LENGTH=128 * 1024,
        WTF_CSRF_TIME_LIMIT=3600, SESSION_TTL=86400,
    )
    settings = os.environ.get('NOTE_DEMO_CONFIG')
    if settings:
        with open(settings, encoding='utf-8') as stream:
            app.config.update(json.load(stream))
    if test_config:
        app.config.update(test_config)
    if not app.config['SECRET_KEY'] or len(app.config['SECRET_KEY']) < 32:
        raise RuntimeError('NOTE_DEMO_CONFIG에 32자 이상의 SECRET_KEY 설정이 필요합니다.')
    db_path = app.config['DATABASE_PATH']
    if not db_path or not Path(db_path).is_absolute():
        raise RuntimeError('DATABASE_PATH는 절대 경로여야 합니다.')
    if app.config['DEPLOYMENT']:
        app.config.update(SESSION_COOKIE_SECURE=True, DEBUG=False)
    csrf.init_app(app)

    from . import db, auth, posts, admin
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(posts.bp)
    app.register_blueprint(admin.bp)
    @app.before_request
    def maintenance():
        from flask import g
        g.user = None
        if Path(str(app.config['DATABASE_PATH']) + '.maintenance').exists():
            abort(503)

    app.before_request(auth.load_user)

    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'same-origin'
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; style-src 'self'; script-src 'self'; "
            "img-src 'self' data:; font-src 'self'; object-src 'none'; "
            "base-uri 'self'; frame-ancestors 'none'; form-action 'self'"
        )
        if not request.path.startswith('/static/'):
            response.headers['Cache-Control'] = 'no-store'
        if app.config['DEPLOYMENT']:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000'
        return response

    def error_page(error):
        code = getattr(error, 'code', 500)
        messages = {400: '요청을 확인해 주세요. 화면을 새로고침한 뒤 다시 시도할 수 있어요.',
                    403: '이 작업을 할 수 있는 권한이 없어요.',
                    404: '요청한 글이나 페이지를 찾을 수 없어요.',
                    405: '지원하지 않는 요청 방식이에요.',
                    413: '입력한 내용이 너무 길어요.',
                    429: '시도가 너무 많아요. 잠시 후 다시 시도해 주세요.',
                    500: '처리 중 문제가 생겼어요. 잠시 후 다시 시도해 주세요.',
                    503: '잠시 정리 중이에요. 조금 뒤에 다시 방문해 주세요.'}
        return render_template('error.html', code=code, message=messages.get(code, messages[500])), code

    for code in (400, 403, 404, 405, 413, 429, 500, 503):
        app.register_error_handler(code, error_page)
    app.register_error_handler(CSRFError, error_page)

    @app.errorhandler(sqlite3.OperationalError)
    def database_error(error):
        app.logger.error('Database operation failed: %s', type(error).__name__)
        return render_template('error.html', code=503,
                               message='저장소가 준비 중이거나 사용 중이에요. 잠시 후 다시 시도해 주세요.'), 503

    return app
