"""Create private configuration once; does not create/delete database content."""
import argparse
import json
import os
import secrets
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--data-dir', required=True, help='Data directory; outside source directory for deployment')
parser.add_argument('--deployment', action='store_true')
args = parser.parse_args()
folder = Path(args.data_dir).expanduser().resolve()
folder.mkdir(parents=True, exist_ok=True)
config = folder / 'config.json'
if config.exists():
    print(f'기존 설정 유지: {config}')
    raise SystemExit(0)
settings = {'SECRET_KEY': secrets.token_hex(32),
            'DATABASE_PATH': str(folder / 'note-demo.sqlite3'),
            'DEPLOYMENT': args.deployment}
with config.open('x', encoding='utf-8') as stream:
    json.dump(settings, stream, indent=2)
if os.name == 'posix':
    folder.chmod(0o700)
    config.chmod(0o600)
print(f'설정 생성: {config}')
print('NOTE_DEMO_CONFIG에 이 파일의 절대 경로를 지정하세요. 비밀키는 출력하지 않습니다.')
