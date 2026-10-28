"""Validate and execute the source archive in an isolated temporary directory."""
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

root = Path(__file__).resolve().parents[1]
archive_path = root / 'dist' / 'note-demo-pythonanywhere.zip'
with tempfile.TemporaryDirectory(prefix='note-demo-package-') as temporary:
    destination = Path(temporary).resolve()
    with ZipFile(archive_path) as archive:
        for name in archive.namelist():
            parts = Path(name).parts
            if any(part in ('.runtime', '.venv', '__pycache__') for part in parts):
                raise RuntimeError('Runtime directory found in archive')
            if name.endswith(('.sqlite3', '.db', 'config.json', '.pyc')):
                raise RuntimeError('Private runtime file found in archive')
            if not (destination / name).resolve().is_relative_to(destination):
                raise RuntimeError('Unsafe archive member')
        archive.extractall(destination)
    env = dict(os.environ)
    env.pop('NOTE_DEMO_CONFIG', None)
    env.pop('PYTHONPATH', None)
    result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                            cwd=destination, env=env)
    if result.returncode:
        raise SystemExit(result.returncode)
print('PACKAGE_OK: source-only archive, isolated tests and WSGI import passed.')
