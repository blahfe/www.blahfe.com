#!/usr/bin/env python3
"""Publish the committed root-site build to the organization Pages repository."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run(*args, cwd=ROOT):
    return subprocess.check_output(args, cwd=cwd, text=True).strip()

if run('git', 'status', '--porcelain'):
    sys.exit('Commit source and generated docs before publishing.')
source_commit = run('git', 'rev-parse', 'HEAD')
subprocess.run([sys.executable, 'scripts/build.py'], cwd=ROOT, check=True)
if run('git', 'status', '--porcelain', '--', 'docs'):
    sys.exit('Build changed docs; commit generated output before publishing.')
with tempfile.TemporaryDirectory(prefix='blahfe-pages-') as temporary:
    target = Path(temporary) / 'site'
    subprocess.run(['git', 'clone', 'git@github.com:blahfe/blahfe.github.io.git', str(target)], check=True)
    for item in target.iterdir():
        if item.name != '.git':
            shutil.rmtree(item) if item.is_dir() else item.unlink()
    shutil.copytree(ROOT / 'docs', target, dirs_exist_ok=True)
    (target / 'source.json').write_text(json.dumps({
        'repository': 'https://github.com/blahfe/www.blahfe.com',
        'commit': source_commit,
    }, indent=2) + '\n')
    run('git', 'checkout', '-B', 'main', cwd=target)
    run('git', 'add', '--all', cwd=target)
    if run('git', 'status', '--porcelain', cwd=target):
        run('git', 'commit', '-m', 'Publish website from ' + source_commit[:12], cwd=target)
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], cwd=target, check=True)
print('Published source ' + source_commit + ' to https://blahfe.github.io/; verify the Pages build.')
