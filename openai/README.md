# FairValid for ChatGPT and Codex

This package connects FairValid's hosted MCP service using OAuth Dynamic Client
Registration. It includes the existing FairValid orange icon and a workflow for
authorized email verification. Contact: nayeem@fairvalid.com.

Endpoint: `https://mcp.fairvalid.com/mcp`
Documentation: https://fairvalid.com/help/mcp
Intended distribution source: https://github.com/moonlitnayeem/fairvalid-ai

The package contains no credentials and performs no installation scripts or
lifecycle hooks. The selected FairValid live API key determines workspace,
permissions, and spending cap. OAuth does not provide sandbox mode.

## Package status

The five positive and three negative cases in `plugin.json` are planned reviewer
scenarios, not execution evidence. Some require a dedicated review workspace,
reviewer-owned addresses, and deliberate authorization to spend credits. No
reviewer credentials, walkthrough recording, or completed native test results
are supplied by this package. Do not represent packaging or a public endpoint
smoke test as directory submission or acceptance.

The current OpenAI packaging guide documents per-server
`extensions.com.openai.auth` in `mcp.json`. The canonical Agent Plugins 1.0.0 MCP
schema currently disallows that field. This package follows OpenAI's documented
OAuth format. Validation records the full-schema incompatibility explicitly,
checks the portable core separately, and checks the documented OpenAI fields.
Portal upload and scan remain necessary to resolve importer acceptance.

## Public-review prerequisites

- Verified publisher identity and any exact domain-verification challenge
  requested by the OpenAI portal.
- A dedicated review account and sample workspace, entered only through the
  secure reviewer-access form; sign-in must meet the portal's requirements.
- Execution and evidence for all five positive and three negative cases with
  that account. Paid operations require explicit authorization and actual owned
  review mailboxes; reserved sandbox fixtures must not be used through OAuth.
- An accessible walkthrough recording demonstrating the cases; add its genuine
  URL only after recording. No placeholder URL is included.
- Connection scan, required attestations, and an actual submission receipt.

The archive builder lives outside this package under `../validation/` and uses
an explicit allowlist. The package files are placed directly at ZIP root.

## License and brand

The package software and documentation are distributed under the [MIT License](LICENSE).
FairValid names and logos identify the original publisher. The license grants
no trademark rights or permission to imply affiliation or endorsement.

Sources reviewed on 30 October 2026:

- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/deploy/submission
- https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
- https://agent-plugins.org/schemas/1.0.0/mcp.schema.json
