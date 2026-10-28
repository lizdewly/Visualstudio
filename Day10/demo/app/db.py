import json
import sqlite3
from contextlib import closing
from pathlib import Path

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        path = Path(current_app.config['DATABASE_PATH'])
        if not path.is_file():
            raise sqlite3.OperationalError('Initialize the database first.')
        g.db = sqlite3.connect(path, timeout=5)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db


def close_db(_error=None):
    conn = g.pop('db', None)
    if conn is not None:
        conn.close()


def initialize():
    path = Path(current_app.config['DATABASE_PATH'])
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path)) as conn:
        with conn:
            conn.executescript(Path(__file__).with_name('schema.sql').read_text(encoding='utf-8'))


def backup_to(destination):
    destination = Path(destination).resolve()
    if destination.exists():
        raise click.ClickException('기존 파일을 덮어쓰지 않습니다. 새 백업 경로를 선택하세요.')
    destination.parent.mkdir(parents=True, exist_ok=True)
    target = sqlite3.connect(destination)
    try:
        get_db().backup(target)
    finally:
        target.close()
    return destination


def init_app(app):
    app.teardown_appcontext(close_db)

    @app.cli.command('init-db')
    def init_db_command():
        """Create missing tables without deleting existing data."""
        initialize()
        click.echo('DB 준비 완료. 기존 데이터는 유지됩니다.')

    @app.cli.command('seed-rules')
    def seed_rules():
        """Explicitly import initial rules; never runs on startup."""
        from .masking import normalize_keyword
        source = Path(app.root_path).parent / 'seed' / 'masking-rules.json'
        items = json.loads(source.read_text(encoding='utf-8'))['keywords']
        conn = get_db()
        before = conn.total_changes
        with conn:
            for keyword in items:
                conn.execute('INSERT OR IGNORE INTO masking_rules(keyword, normalized_keyword) VALUES (?,?)',
                             (keyword, normalize_keyword(keyword)))
        click.echo(f'{conn.total_changes - before}개 규칙을 추가했습니다. 재시작 시 자동 복원하지 않습니다.')

    @app.cli.command('backup-db')
    @click.argument('destination', type=click.Path())
    def backup_command(destination):
        """Create a consistent SQLite backup at a NEW path."""
        click.echo(f'백업 완료: {backup_to(destination)}')

    @app.cli.command('restore-db')
    @click.argument('source', type=click.Path(exists=True, dir_okay=False))
    @click.option('--confirm', is_flag=True, help='Explicitly confirm restore after stopping the web app.')
    def restore_command(source, confirm):
        """Restore while web app is disabled and maintenance marker exists."""
        from datetime import datetime, timezone
        path = Path(app.config['DATABASE_PATH'])
        if not confirm or not Path(str(path) + '.maintenance').exists():
            raise click.ClickException('웹앱을 비활성화하고 DB 경로 + .maintenance 파일을 만든 뒤 --confirm을 사용하세요.')
        if Path(source).resolve() == path.resolve():
            raise click.ClickException('현재 DB를 복구 원본으로 사용할 수 없습니다.')
        uri = Path(source).resolve().as_uri() + '?mode=ro'
        src = sqlite3.connect(uri, uri=True)
        try:
            if src.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                raise click.ClickException('백업 무결성 검사 실패')
            if src.execute('SELECT version FROM schema_meta').fetchall() != [(1,)]:
                raise click.ClickException('지원하지 않는 스키마 버전입니다.')
            required = {'users', 'sessions', 'posts', 'comments', 'masking_rules', 'auth_attempts'}
            tables = {r[0] for r in src.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if not required.issubset(tables) or src.execute('PRAGMA foreign_key_check').fetchall():
                raise click.ClickException('백업 테이블 또는 관계 검사 실패')
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
            if path.exists():
                backup_to(str(path) + f'.before-restore-{stamp}')
            close_db()
            dst = sqlite3.connect(path)
            try:
                src.backup(dst)
                with dst:
                    dst.execute('DELETE FROM sessions')
                    dst.execute('DELETE FROM auth_attempts')
            finally:
                dst.close()
        finally:
            src.close()
        click.echo('복구 완료. 세션을 폐기했습니다. 점검 후 유지보수 파일을 제거하고 웹앱을 활성화하세요.')
