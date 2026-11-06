# Package validation

Validation date: **6 November 2026**. Distribution version: **1.1.0**.

**Production API/MCP acceptance recorded.** The deployed service passed public
checks and controlled production Test-key acceptance. Package checks and provider
publication are separate: this record does not claim new native-client OAuth or
tool execution, paid live acquisition, or approval in every marketplace.

| Check | Observed result |
| --- | --- |
| `python3 validation/validate_packages.py` | Passed: 20 JSON files, 5 TOML files, matching 1.1.0 metadata, all local Markdown targets, four matching FairMatch skills, explicit OpenAI lead scopes and nine default tools for OpenClaw/Hermes, including all six FairMatch tools. |
| Claude Code 2.1.312, `claude plugin validate <repo> --strict` | Passed; no warnings/errors. |
| Claude Code 2.1.312, `claude plugin validate <repo>/claude --strict --profile directory` | Passed; no warnings/errors. Includes both workflow skills. |
| `server.json`, official 2025-12-11 MCP Registry schema; Ajv 8.20.0/ajv-formats 3.0.1 | Passed. |
| `openai/plugin.json`, current Agent Plugins 1.0.0 schema | Passed. |
| Full `openai/mcp.json` against current portable MCP schema | Known incompatibility remains: its HTTP branch rejects documented OpenAI per-server `extensions`. It is not described as a full-schema pass. |
| OpenAI portable MCP core plus documented DCR/baseScopes fields | Passed separately; requires actual portal import/scan before importer acceptance can be claimed. |
| Zed `cargo test --locked --offline`, Rust 1.99.1 | Passed all three existing path/transport/OAuth-cache helper tests. No connection/model execution. |
| Zed `cargo build --locked --offline --release --target wasm32-wasip2` | Passed. Rebuilt because installation instructions are embedded in WASM. No native Zed test of 1.1.0. |
| Version/source review | Original 1.0.0 release/tag remains unchanged. Zed package/crate/lock version updated consistently to 1.1.0; transport code and pinned bridge unchanged. |
| ClawHub CLI 0.24.1 package inspector, target OpenClaw 2026.11.1 | Passed with zero issues/warnings; metadata inspection only, not native OAuth or tool execution. Reports kept outside the bundle. |
| `python3 validation/build_archives.py --worktree` | Dedicated archive allowlists and byte readback: Claude 8 files, OpenAI 10, OpenClaw 8. Preparation archives record no source commit. |

## Acceptance state

| Evidence | Current state |
| --- | --- |
| Production revision and API/MCP acceptance | Revision `08424974ccd394fc16139a85216c4cc0afc1a067`, accepted November 6, 2026 at 12:46:06 UTC. 15 public checks and 23 controlled production Test-key checks passed. |
| Controlled synthetic execution | Six FairMatch tools through REST/MCP plus five legacy operations; catalog contains 12 tools. Three fictional contacts produced two deliveries and one unavailable result, zero charged credits and no live acquisition dispatch. REST-to-MCP unchanged retry returned the same batch. The temporary key was revoked; subsequent REST/MCP requests were denied. |
| Fresh OAuth consent and unchanged existing grants | Deployed fresh omitted-scope authorization requests all six scopes through explicit consent. Regression coverage preserves explicit old-scope requests and existing grant/refresh scopes. This is not new native-client OAuth acceptance. |
| Exact public 1.1.0 source commit and release archives | The v1.1.0 tag and release assets identify the final distribution source. Reproducible archives contain 8 Claude, 10 OpenAI and 8 OpenClaw files. |
| 1.1.0 provider publication and native execution | Not established by these checks; record each provider separately. |

Provider updates retain their own submission, review and publication evidence.
The [release procedure](validation/RELEASE-1.1.0.md) keeps publication and source-pin
updates separate from production acceptance.

The new FairMatch contracts were checked against the owning implementation:
filter discovery; 1–50 selections; `maximumCredits` 0–200; MCP `confirm: true`;
idempotent unlock; original-key batch retrieval; five-to-thirty-second polling;
100-contact saved pages; and synthetic fixture expectations. This was a source
check. The controlled production sandbox execution is recorded separately above;
it is not a paid live acquisition test. Existing permission grants are not expanded
by package metadata. No credential is included in the distribution.

The Claude validator explicitly excludes the directory safety scan and policy
review. Provider-specific metadata outside a generic portable schema is checked
against the provider's documentation and remains subject to its importer.

## Reproduce the package checks

Run `python3 validation/validate_packages.py` from a Python 3.11+ environment.
For JSON Schema checks, fetch these official schemas into ignored
`validation/.cache/schemas/` as `registry.json`, `plugin.json`, and `mcp.json`:

- https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json
- https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
- https://agent-plugins.org/schemas/1.0.0/mcp.schema.json

Then run `node validation/validate_schemas.cjs /path/to/ajv /path/to/ajv-formats`
using Ajv 8.20.0 and ajv-formats 3.0.1. That script explicitly checks the selected
HTTP branch and portable core rather than suppressing unexpected schema errors.
Local CLI/schema checks do not open OAuth or install the package in a host.

For Zed, run the two commands above from `zed/` with Rust 1.99.1 and cached locked
dependencies. The recorded run used a task-local copy of the existing dependency
cache and kept build output under ignored `validation/.cache/`; it installed no
new client or global toolchain and made no model or FairValid business calls.

## Release prerequisites

Production API/MCP and synthetic acceptance passed. Release the exact reviewed
source and archive allowlists, and record each actual provider update separately.
Reauthorization for lead scopes must be deliberate. A live acquisition test
requires separate owner approval of the exact selection and numerical ceiling;
no automatic customer-contact acquisition is permitted by package installation.

## Historical 1.0.0 structure checks

Validation date: **30 October 2026**. Distribution version: **1.0.0**.

This record covers package structure and metadata. It does not certify native
client authentication, live tool calls, marketplace acceptance, or publication.

| Check | Observed result |
| --- | --- |
| Claude Code 2.1.312, `claude plugin validate <catalog> --strict` | Passed; no warnings or errors |
| Claude Code 2.1.312, `claude plugin validate <catalog>/.claude-plugin/plugin.json --strict` | Passed; no warnings or errors |
| All JSON files parsed with Python `json.loads` | Passed |
| Grok example parsed with Python `tomllib.loads` | Passed |
| `server.json` checked by Ajv 8.20.0 and ajv-formats 3.0.1 against the official 2025-12-11 MCP Registry schema | Passed; zero errors |
| Local Markdown link targets | All present |
| Source icon compared with the existing FairValid web brand asset | Identical SVG reused |
| PNG output generated by sharp 0.35.5 | Confirmed PNG at 400×400, 512×512, and 1024×1024; 400-pixel image visually inspected |
| FairValid MCP/API documentation, privacy, terms, contact, and hosted icon URLs | All returned HTTP 200 |

The Claude validator covers only part of directory acceptance. Its output
explicitly excludes the directory's safety scan and policy review.

## Metadata references

- [Claude plugin manifest and directory metadata](https://code.claude.com/docs/en/plugins-reference)
- [Claude install command and supported versions](https://code.claude.com/docs/en/discover-plugins#add-a-marketplace-and-install-in-one-command)
- [Cursor plugin format](https://cursor.com/docs/reference/plugins)
- [Gemini extension manifest](https://geminicli.com/docs/extensions/reference/)
- [Gemini HTTP transport and automatic OAuth](https://geminicli.com/docs/tools/mcp-server/)
- [Grok support for Claude-compatible plugins](https://docs.x.ai/build/features/skills-plugins-marketplaces)
- [MCP Registry remote server publishing](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/remote-servers.mdx)
- [MCP Registry JSON schema](https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json)
- [Client example references](examples/README.md)

The endpoint, tool names and scope requirements, idempotency behavior, billing
semantics, OAuth Live-key restriction, and safe sandbox behavior were checked
against FairValid's owning implementation documentation for this release.

## Remaining acceptance evidence

The package was not installed into any host's settings during these checks.
The controlled Test-key API/MCP calls above do not establish a native client's
OAuth or model-driven execution. No paid live acquisition was performed for this
release acceptance. Each provider's native workflow must be exercised and
recorded before claiming it passed.
Public listings and review outcomes must be tracked separately from this package.

## OpenAI 1.1.1 importer compatibility patch

On November 6, 2026, the live OpenAI importer required exactly five positive and
three negative review cases. Package 1.1.1 groups the planned scenarios into
those counts while preserving coverage of all twelve tools and explicit spend,
cancellation, workspace, permission and safe-retry boundaries. Pricing is removed
from the OpenAI listing description. The ten-file archive, runtime endpoint and
six requested OAuth scopes are unchanged. Other provider packages remain 1.1.0.

These metadata checks do not execute the planned native-client review scenarios.
The recorded 23-check production Test-key acceptance remains API/MCP evidence,
not proof that the OpenAI review cases passed.
