#!/usr/bin/env python3
"""Check coordinated FairValid distribution metadata without loading a client."""
from pathlib import Path
import json
import re
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[1]
VERSION = '1.1.0'
MCP_URL = 'https://mcp.fairvalid.com/mcp'
paths = subprocess.check_output(
    ['git', 'ls-files', '--cached', '--others', '--exclude-standard'],
    cwd=ROOT, text=True,
).splitlines()
files = [ROOT / name for name in dict.fromkeys(paths) if (ROOT / name).is_file()]
json_docs = {str(p.relative_to(ROOT)): json.loads(p.read_text()) for p in files if p.suffix == '.json'}
toml_docs = {str(p.relative_to(ROOT)): tomllib.loads(p.read_text()) for p in files if p.suffix == '.toml' or p.name == 'Cargo.lock'}

for name in [
    '.claude-plugin/plugin.json', 'claude/.claude-plugin/plugin.json',
    '.cursor-plugin/plugin.json', 'gemini-extension.json', 'server.json',
    'openai/plugin.json', 'openclaw/package.json', 'openclaw/.claude-plugin/plugin.json',
]:
    assert json_docs[name]['version'] == VERSION, name
assert json_docs['.claude-plugin/marketplace.json']['plugins'][0]['version'] == VERSION
assert json_docs['.claude-plugin/marketplace.json']['plugins'][0]['source'] == './claude'
assert toml_docs['zed/extension.toml']['version'] == VERSION
assert toml_docs['zed/Cargo.toml']['package']['version'] == VERSION
crate = next(p for p in toml_docs['zed/Cargo.lock']['package'] if p['name'] == 'fairvalid_mcp_server')
assert crate['version'] == VERSION
assert json_docs['server.json']['remotes'] == [{'type': 'streamable-http', 'url': MCP_URL}]

expected_scopes = ['read', 'submit', 'balance', 'leads:read', 'leads:acquire', 'offline_access']
auth = json_docs['openai/mcp.json']['mcpServers']['fairvalid']['extensions']['com.openai']['auth']
assert auth == {'type': 'oauth', 'client': {'mode': 'dcr'}, 'baseScopes': expected_scopes}
default_tools = [
    'fairvalid_get_balance', 'fairvalid_get_job', 'fairvalid_get_results',
    'fairvalid_get_lead_filters', 'fairvalid_search_leads', 'fairvalid_quote_leads',
    'fairvalid_unlock_leads',
    'fairvalid_get_lead_batch', 'fairvalid_get_leads',
]
assert json_docs['openclaw/.mcp.json']['mcpServers']['fairvalid']['toolFilter']['include'] == default_tools
hermes = re.findall(r'^        - (fairvalid_[a-z_]+)$', (ROOT / 'examples/hermes.yaml').read_text(), re.M)
assert hermes == default_tools
assert 'fairvalid_unlock_leads' in default_tools
assert len(default_tools) == len(set(default_tools)) == 9
assert json_docs['openclaw/.mcp.json']['mcpServers']['fairvalid']['auth'] == 'oauth'

skill_paths = [
    'skills/fairmatch-leads/SKILL.md', 'claude/skills/fairmatch-leads/SKILL.md',
    'openai/skills/fairmatch-leads/SKILL.md', 'openclaw/skills/fairmatch-leads/SKILL.md',
]
canonical = (ROOT / skill_paths[0]).read_bytes()
for name in skill_paths:
    assert (ROOT / name).read_bytes() == canonical, name
    assert canonical.startswith(b'---\nname: fairmatch-leads\n')
assert b'maximumCredits' in canonical and b'confirm: true' in canonical
assert b'leads:read' in canonical and b'leads:acquire' in canonical

for plugin_root, manifest in [
    (ROOT, json_docs['.claude-plugin/plugin.json']),
    (ROOT / 'claude', json_docs['claude/.claude-plugin/plugin.json']),
    (ROOT / 'openclaw', json_docs['openclaw/.claude-plugin/plugin.json']),
]:
    assert (plugin_root / manifest['icon']).is_file()
overlay = json_docs['openai/plugin.json']['extensions']['com.openai']
for value in [overlay['onboardingSkill'], overlay['interface']['composerIcon'], overlay['interface']['logo']]:
    assert (ROOT / 'openai' / value).is_file()
cases = overlay['review']['test_cases']
assert len(cases['positive']) == 8 and len(cases['negative']) == 5

link_count = 0
for file in files:
    if file.suffix != '.md':
        continue
    for raw in re.findall(r'\]\(([^)]+)\)', file.read_text()):
        target = raw.strip('<>').split('#', 1)[0]
        if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
            continue
        assert (file.parent / target).exists(), f'Missing link: {file.relative_to(ROOT)} -> {target}'
        link_count += 1

print(json.dumps({
    'distribution_version': VERSION,
    'json_files_parsed': len(json_docs), 'toml_files_parsed': len(toml_docs),
    'local_markdown_links': link_count, 'matching_fairmatch_skills': len(skill_paths),
    'default_tools': len(default_tools),
    'fairmatch_acquisition_tool_available': True,
    'metadata_scope_filter_reference_checks': 'passed',
    'network_or_authentication_performed': False,
    'native_fairmatch_acceptance_claimed': False,
}, indent=2))
