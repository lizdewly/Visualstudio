"""Local-only launcher. PythonAnywhere uses wsgi.py instead."""
import os
from pathlib import Path

from app import create_app

if __name__ == '__main__':
    config = Path(__file__).resolve().parent / '.runtime' / 'config.json'
    os.environ.setdefault('NOTE_DEMO_CONFIG', str(config))
    create_app().run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
