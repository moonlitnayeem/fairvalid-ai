#!/usr/bin/env python3
"""Build allowlisted review/release ZIPs without publishing or accessing credentials."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    'claude': [
        '.claude-plugin/plugin.json', '.mcp.json', 'BRAND.md', 'LICENSE', 'README.md',
        'assets/fairvalid-icon-512.png', 'skills/email-verification/SKILL.md',
        'skills/fairmatch-leads/SKILL.md',
    ],
    'openai': [
        'LICENSE', 'README.md', 'assets/fairvalid-icon-1024.png',
        'assets/fairvalid-icon-128.png', 'assets/fairvalid-icon-512.png',
        'assets/fairvalid-icon.svg', 'mcp.json', 'plugin.json',
        'skills/verify-emails/SKILL.md', 'skills/fairmatch-leads/SKILL.md',
    ],
    'openclaw': [
        '.claude-plugin/plugin.json', '.mcp.json', 'LICENSE', 'README.md',
        'assets/icon.png', 'package.json',
        'skills/fairvalid-email-verification/SKILL.md', 'skills/fairmatch-leads/SKILL.md',
    ],
}


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def source_files(package, commit):
    if commit:
        records = git('ls-tree', '-rz', '--full-tree', commit, package).split(b'\0')
        result = {}
        for record in filter(None, records):
            metadata, raw_name = record.split(b'\t', 1)
            mode, kind, object_id = metadata.decode().split()
            name = raw_name.decode().removeprefix(package + '/')
            if mode != '100644' or kind != 'blob':
                raise ValueError('Unexpected file mode: ' + name)
            result[name] = git('cat-file', 'blob', object_id)
    else:
        result = {}
        for path in (ROOT / package).rglob('*'):
            if path.is_symlink():
                raise ValueError('Unexpected symlink: ' + str(path))
            if path.is_file():
                result[path.relative_to(ROOT / package).as_posix()] = path.read_bytes()
    if set(result) != set(FILES[package]):
        raise ValueError(f'{package}: unexpected/missing files: {sorted(set(result) ^ set(FILES[package]))}')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--worktree', action='store_true', help='Review only; records no source commit')
    source.add_argument('--commit', help='Full 40-character source commit; does not attest acceptance')
    args = parser.parse_args()
    if args.commit and not re.fullmatch('[0-9a-f]{40}', args.commit):
        parser.error('--commit must be a full lowercase Git commit SHA')
    output = ROOT / 'validation/.cache/archives'
    output.mkdir(parents=True, exist_ok=True)
    receipts = []
    for package in FILES:
        files = source_files(package, args.commit)
        manifest = json.loads(files['plugin.json' if package == 'openai' else '.claude-plugin/plugin.json'])
        version = manifest['version']
        if not re.fullmatch(r'\d+\.\d+\.\d+', version):
            raise ValueError('Expected stable semantic version')
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w', compression=zipfile.ZIP_STORED) as archive:
            for name, raw in sorted(files.items()):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, raw)
        payload = data.getvalue()
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            assert {name: archive.read(name) for name in archive.namelist()} == files
        suffix = '-preparation' if args.worktree else ''
        path = output / f'fairvalid-{package}-{version}{suffix}.zip'
        path.write_bytes(payload)
        receipts.append({'archive': path.name, 'version': version, 'source_commit': args.commit,
                         'source_path': package, 'review_only': args.worktree,
                         'files': sorted(files), 'bytes': len(payload),
                         'sha256': hashlib.sha256(payload).hexdigest()})
    receipt_path = output / ('preparation-archives.json' if args.worktree else 'release-archives.json')
    receipt_path.write_text(json.dumps(receipts, indent=2) + '\n')
    print(json.dumps(receipts, indent=2))


if __name__ == '__main__':
    main()
