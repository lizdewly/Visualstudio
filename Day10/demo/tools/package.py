"""Build a source-only deployment zip; excludes all live configuration/data."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
destination = root / 'dist' / 'note-demo-pythonanywhere.zip'
destination.parent.mkdir(exist_ok=True)
files = [root / name for name in ('requirements.txt', 'wsgi.py', 'run.py', 'README.md')]
for folder in ('app', 'seed', 'tools', 'docs', 'tests'):
    files.extend(p for p in (root / folder).rglob('*') if p.is_file()
                 and '__pycache__' not in p.parts and p.suffix not in ('.pyc', '.sqlite3', '.db', '.png'))
with ZipFile(destination, 'w', ZIP_DEFLATED) as archive:
    for path in sorted(files):
        archive.write(path, path.relative_to(root))
print(f'배포 패키지: {destination} ({len(files)} files)')
