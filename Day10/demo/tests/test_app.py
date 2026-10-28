import json
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from werkzeug.security import check_password_hash, generate_password_hash

from app import create_app
from app.db import get_db, initialize, backup_to
from app.masking import mask_text

ROOT = Path(__file__).resolve().parents[1]


class AppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.password = 'only-for-tests-123'
        cls.password_hash = generate_password_hash(cls.password)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'data.sqlite3'
        self.config = {'TESTING': True, 'SECRET_KEY': 'test-key-' * 8,
                       'DATABASE_PATH': str(self.path), 'WTF_CSRF_ENABLED': True}
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        with self.app.app_context():
            initialize()
            conn = get_db()
            with conn:
                for user, role in [('a', 'USER'), ('b', 'USER'), ('admin', 'ADMIN')]:
                    conn.execute('INSERT INTO users(email,nickname,password_hash,role) VALUES (?,?,?,?)',
                                 (f'{user}@example.com', user, self.password_hash, role))

    def tearDown(self):
        self.temp.cleanup()

    def csrf(self, path='/login', client=None):
        client = client or self.client
        page = client.get(path)
        token = re.search(r'name="csrf_token" value="([^"]+)"', page.get_data(as_text=True))
        self.assertIsNotNone(token, path)
        return token.group(1)

    def post(self, path, data=None, form='/login', client=None, **kwargs):
        client = client or self.client
        payload = dict(data or {})
        payload['csrf_token'] = self.csrf(form, client)
        return client.post(path, data=payload, **kwargs)

    def login(self, user='a', client=None):
        return self.post('/login', {'email': f'{user}@example.com', 'password': self.password}, client=client)

    def add_posts(self, count, author=1):
        with self.app.app_context():
            conn = get_db()
            with conn:
                for i in range(count):
                    conn.execute('INSERT INTO posts(author_id,title_raw,content_raw) VALUES (?,?,?)',
                                 (author, f'제목 {i:02d}', f'본문은 목록에 나오면 안 됨 {i}'))

    def test_signup_validation_hash_duplicate_and_persistence(self):
        response = self.post('/signup', {'email': 'new@example.com', 'nickname': '새이름', 'password': self.password}, form='/signup')
        self.assertEqual(response.status_code, 303)
        with self.app.app_context():
            user = get_db().execute('SELECT * FROM users WHERE email=?', ('new@example.com',)).fetchone()
            self.assertNotEqual(user['password_hash'], self.password)
            self.assertTrue(check_password_hash(user['password_hash'], self.password))
            self.assertEqual(user['role'], 'USER')
        self.assertEqual(self.post('/signup', {'email': 'NEW@example.com', 'nickname': '다른이름', 'password': self.password}, form='/signup').status_code, 400)
        self.assertEqual(self.post('/signup', {'email': 'bad', 'nickname': '', 'password': 'short'}, form='/signup').status_code, 400)
        restarted = create_app(self.config).test_client()
        self.assertEqual(self.post('/login', {'email': 'new@example.com', 'password': self.password}, client=restarted).status_code, 303)

    def test_login_failure_and_logout_replay(self):
        self.assertEqual(self.post('/login', {'email': 'a@example.com', 'password': 'wrong-password'}).status_code, 400)
        self.assertEqual(self.login().status_code, 303)
        old = self.client.get_cookie('session').value
        self.assertEqual(self.post('/logout', form='/posts').status_code, 303)
        self.client.set_cookie('session', old)
        self.assertEqual(self.client.get('/posts/new').status_code, 302)

    def test_expired_session(self):
        self.login()
        with self.app.app_context():
            conn = get_db()
            with conn:
                conn.execute('UPDATE sessions SET expires_at=0')
        self.assertEqual(self.client.get('/posts/new').status_code, 302)

    def test_csrf_all_state_changes_and_read_only_get(self):
        self.add_posts(1)
        for route in ['/signup', '/login', '/logout', '/posts/new', '/posts/1/edit', '/posts/1/delete', '/posts/1/comments', '/admin/masking', '/admin/masking/1/delete']:
            self.assertEqual(self.client.post(route, data={}).status_code, 400, route)
        self.assertEqual(self.client.get('/posts/1/delete').status_code, 405)

    def test_ownership_direct_calls_and_spoofed_author(self):
        self.add_posts(1)
        self.login('b')
        self.assertEqual(self.client.get('/posts/1/edit').status_code, 403)
        for route in ['/posts/1/edit', '/posts/1/delete']:
            response = self.post(route, {'title': '침입', 'content': '침입', 'confirm': 'yes'}, form='/posts')
            self.assertEqual(response.status_code, 403)
        self.assertEqual(self.post('/posts/new', {'title': 'B의 글', 'content': '본문', 'author_id': 1}, form='/posts/new').status_code, 303)
        with self.app.app_context():
            self.assertEqual(get_db().execute('SELECT author_id FROM posts WHERE id=2').fetchone()[0], 2)
        self.post('/logout', form='/posts')
        self.login('admin')
        self.assertEqual(self.post('/posts/1/delete', {'confirm': 'yes'}, form='/posts').status_code, 403)

    def test_post_crud_blank_missing_and_cascade(self):
        self.login()
        self.assertEqual(self.post('/posts/new', {'title': ' ', 'content': ' '}, form='/posts/new').status_code, 400)
        self.assertEqual(self.post('/posts/new', {'title': '새 글', 'content': '내용'}, form='/posts/new').status_code, 303)
        self.assertEqual(self.post('/posts/1/edit', {'title': '수정된 글', 'content': '수정 내용'}, form='/posts/1/edit').status_code, 303)
        self.assertIn('수정된 글', self.client.get('/posts/1').get_data(as_text=True))
        self.assertEqual(self.post('/posts/1/comments', {'content': '댓글'}, form='/posts/1').status_code, 303)
        confirm = self.post('/posts/1/delete', form='/posts/1')
        self.assertEqual(confirm.status_code, 200)
        self.assertIn('지울까요?', confirm.get_data(as_text=True))
        self.assertEqual(self.post('/posts/1/delete', {'confirm': 'yes'}, form='/posts/1').status_code, 303)
        self.assertEqual(self.client.get('/posts/1').status_code, 404)
        with self.app.app_context():
            self.assertEqual(get_db().execute('SELECT COUNT(*) FROM comments').fetchone()[0], 0)

    def test_pagination_boundaries_order_and_deleted_last_page(self):
        for count in [0, 1, 10, 11, 21]:
            with self.subTest(count=count):
                with self.app.app_context():
                    conn = get_db()
                    with conn:
                        conn.execute('DELETE FROM posts')
                self.add_posts(count)
                seen = []
                pages = max(1, (count + 9) // 10)
                for page in range(1, pages + 1):
                    html = self.client.get(f'/posts?page={page}').get_data(as_text=True)
                    ids = re.findall(r'<li><a href="/posts/(\d+)\?page=', html)
                    self.assertEqual(len(ids), min(10, max(0, count - 10*(page-1))))
                    self.assertNotIn('본문은 목록', html)
                    seen.extend(ids)
                self.assertEqual(len(set(seen)), count)
                self.assertEqual(seen, sorted(seen, key=int, reverse=True))
        for value in ['0', '-1', 'bad']:
            self.assertIn('<strong>1</strong>', self.client.get('/posts?page=' + value).get_data(as_text=True))
        self.assertIn('<strong>3</strong>', self.client.get('/posts?page=99999').get_data(as_text=True))
        self.login()
        response = self.post('/posts/1/delete', {'confirm': 'yes', 'page': '3'}, form='/posts/1', follow_redirects=True)
        self.assertIn('<strong>2</strong>', response.get_data(as_text=True))

    def test_comments_separation_anonymous_and_blank(self):
        self.add_posts(2)
        self.assertEqual(self.post('/posts/1/comments', {'content': '침입'}).status_code, 403)
        self.login()
        self.assertEqual(self.post('/posts/1/comments', {'content': ' '}, form='/posts/1').status_code, 400)
        self.post('/posts/1/comments', {'content': '유일한댓글'}, form='/posts/1')
        self.assertIn('유일한댓글', self.client.get('/posts/1').get_data(as_text=True))
        self.assertNotIn('유일한댓글', self.client.get('/posts/2').get_data(as_text=True))

    def test_masking_admin_dynamic_rules_and_raw_leak(self):
        self.login()
        self.post('/posts/new', {'title': '금칙어 제목', 'content': '금칙어 <script>alert(1)</script>'}, form='/posts/new')
        self.post('/posts/1/comments', {'content': '댓글 금칙어'}, form='/posts/1')
        self.assertEqual(self.client.get('/admin/masking').status_code, 403)
        self.assertEqual(self.post('/admin/masking', {'keyword': '금칙어'}, form='/posts').status_code, 403)
        self.post('/logout', form='/posts')
        self.login('admin')
        self.assertEqual(self.post('/admin/masking', {'keyword': '금칙어'}, form='/admin/masking').status_code, 303)
        self.assertEqual(self.post('/admin/masking', {'keyword': '금칙어'}, form='/admin/masking').status_code, 400)
        self.assertEqual(self.post('/admin/masking', {'keyword': ' '}, form='/admin/masking').status_code, 400)
        for path in ['/posts', '/posts/1']:
            self.assertNotIn('금칙어', self.client.get(path).get_data(as_text=True))
        html = self.client.get('/posts/1').get_data(as_text=True)
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('<script>alert(1)</script>', html)
        self.assertEqual(self.client.get('/posts/1/edit').status_code, 403)
        self.post('/admin/masking/1/delete', form='/admin/masking')
        self.assertIn('금칙어', self.client.get('/posts/1').get_data(as_text=True))
        self.post('/logout', form='/posts')
        self.login()
        self.assertIn('금칙어', self.client.get('/posts/1/edit').get_data(as_text=True))

    def test_backup_restore_preserves_data_revokes_sessions(self):
        self.add_posts(1)
        self.login()
        old_cookie = self.client.get_cookie('session').value
        source = Path(self.temp.name) / 'backup.sqlite3'
        with self.app.app_context():
            backup_to(source)
            conn = get_db()
            with conn:
                conn.execute('DELETE FROM posts')
        marker = Path(str(self.path) + '.maintenance')
        marker.touch()
        runner = self.app.test_cli_runner()
        result = runner.invoke(args=['restore-db', str(source), '--confirm'])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(self.client.get('/posts').status_code, 503)
        marker.unlink()
        self.client.set_cookie('session', old_cookie)
        self.assertEqual(self.client.get('/posts/new').status_code, 302)
        with self.app.app_context():
            self.assertEqual(get_db().execute('SELECT COUNT(*) FROM posts').fetchone()[0], 1)

    def test_restart_and_seed_not_automatic_and_init_non_destructive(self):
        runner = self.app.test_cli_runner()
        self.assertEqual(runner.invoke(args=['seed-rules']).exit_code, 0)
        self.add_posts(1)
        with self.app.app_context():
            conn = get_db()
            with conn:
                conn.execute('DELETE FROM masking_rules WHERE id=1')
            before = conn.execute('SELECT COUNT(*) FROM masking_rules').fetchone()[0]
            initialize()
        app2 = create_app(self.config)
        with app2.app_context():
            self.assertEqual(get_db().execute('SELECT COUNT(*) FROM posts').fetchone()[0], 1)
            self.assertEqual(get_db().execute('SELECT COUNT(*) FROM masking_rules').fetchone()[0], before)

    def test_wsgi_production_headers_cookie_and_config(self):
        cfg = dict(self.config, DEPLOYMENT=True)
        production = create_app(cfg)
        client = production.test_client()
        response = client.get('/login', base_url='https://example.com')
        self.assertIn('Secure', response.headers['Set-Cookie'])
        self.assertIn('HttpOnly', response.headers['Set-Cookie'])
        self.assertIn('SameSite=Lax', response.headers['Set-Cookie'])
        self.assertIn('Content-Security-Policy', response.headers)
        self.assertFalse(production.debug)
        path = Path(self.temp.name) / 'config.json'
        path.write_text(json.dumps(cfg), encoding='utf-8')
        env = dict(os.environ, NOTE_DEMO_CONFIG=str(path))
        result = subprocess.run([sys.executable, '-c', 'from wsgi import application; assert application.test_client().get("/posts").status_code == 200; print("WSGI_OK")'], cwd=ROOT, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('WSGI_OK', result.stdout)
        for route in ['/config.json', '/data.sqlite3', '/.runtime/config.json']:
            self.assertEqual(client.get(route).status_code, 404)

    def test_missing_config_fails_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError):
                create_app()

    def test_https_login_csrf_and_admin_cli(self):
        production = create_app(dict(self.config, DEPLOYMENT=True))
        client = production.test_client()
        page = client.get('/login', base_url='https://example.com').get_data(as_text=True)
        token = re.search(r'name="csrf_token" value="([^"]+)"', page).group(1)
        payload = {'email': 'a@example.com', 'password': self.password, 'csrf_token': token}
        self.assertEqual(client.post('/login', data=payload, base_url='https://example.com',
                                     headers={'Referer': 'https://evil.example/'}).status_code, 400)
        result = client.post('/login', data=payload, base_url='https://example.com',
                             headers={'Referer': 'https://example.com/login'})
        self.assertEqual(result.status_code, 303)
        self.assertEqual(client.get('/posts/new', base_url='https://example.com').status_code, 200)
        runner = self.app.test_cli_runner()
        result = runner.invoke(args=['auth', 'create-admin', '--email', 'owner@example.com', '--nickname', 'Owner'],
                               input=self.password + '\n' + self.password + '\n')
        self.assertEqual(result.exit_code, 0, result.output)
        with self.app.app_context():
            self.assertEqual(get_db().execute('SELECT role FROM users WHERE email=?', ('owner@example.com',)).fetchone()[0], 'ADMIN')

    def test_throttle_limits_repeated_authentication(self):
        for _ in range(10):
            self.assertEqual(self.post('/login', {'email': 'missing@example.com', 'password': self.password}).status_code, 400)
        self.assertEqual(self.post('/login', {'email': 'missing@example.com', 'password': self.password}).status_code, 429)


class MaskingTest(unittest.TestCase):
    def test_overlaps_repeats_case_and_literals(self):
        self.assertEqual(mask_text('ababa', ['aba', 'bab']), '***')
        self.assertEqual(mask_text('BAD bad', ['bad']), '*** ***')
        self.assertEqual(mask_text('a+b aaab', ['a+b']), '*** aaab')
        self.assertEqual(mask_text('aaa', ['aa']), '***')
        self.assertEqual(mask_text('고양이 새끼가 자라요. 보지 못한 풍경', ['개새끼', '씨발']), '고양이 새끼가 자라요. 보지 못한 풍경')
        self.assertEqual(mask_text('İ BAD 끝', ['bad']), 'İ *** 끝')


if __name__ == '__main__':
    unittest.main()
