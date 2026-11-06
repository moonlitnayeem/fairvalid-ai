# FairValid for ChatGPT and Codex

> **OpenAI package 1.1.1 / FairValid runtime 1.1.0:** FairMatch API/MCP passed controlled production sandbox
> acceptance on November 6, 2026. Provider listings and native-client acceptance
> are tracked separately. Discover the connected server capabilities before use;
> acquisition requires an explicit numerical credit limit and confirmation.


This package connects FairValid's hosted MCP service using OAuth Dynamic Client
Registration. It includes the existing FairValid orange icon and a workflow for
authorized email verification and FairMatch leads. Contact: nayeem@fairvalid.com.

Endpoint: `https://mcp.fairvalid.com/mcp`
Documentation: https://fairvalid.com/help/mcp
Intended distribution source: https://github.com/moonlitnayeem/fairvalid-ai

The package contains no credentials and performs no installation scripts or
lifecycle hooks. The selected FairValid live API key determines workspace,
permissions, and spending cap. OAuth does not provide sandbox mode.

## Package status

OpenAI package 1.1.1 is a review-metadata compatibility patch: the live importer
requires exactly five positive and three negative scenarios. The scenarios group
all twelve tools while retaining separate spend and cancellation confirmations.
The listing description omits pricing; functional credit controls remain in the
skills and review cases. Runtime, OAuth scopes and other provider packages remain
at the accepted 1.1.0 release.

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

Build any review archive from this `openai/` folder with the package files at ZIP
root and both skill directories included. Do not include repository workflows,
other provider packages, credentials or preparation artifacts. The release owner
must record the exact file allowlist and digest before upload.

## License and brand

The package software and documentation are distributed under the [MIT License](LICENSE).
FairValid names and logos identify the original publisher. The license grants
no trademark rights or permission to imply affiliation or endorsement.

Sources reviewed on 30 October 2026:

- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/deploy/submission
- https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
- https://agent-plugins.org/schemas/1.0.0/mcp.schema.json

## FairMatch in version 1.1.0

The package includes the [FairMatch workflow](skills/fairmatch-leads/SKILL.md).
Use `fairvalid_get_lead_filters`, `fairvalid_search_leads` and
`fairvalid_quote_leads` to discover and quote the user's chosen business leads.
`fairvalid_unlock_leads` starts a batch only after explicit confirmation of the
selected people and a numerical `maximumCredits` ceiling. Follow
`fairvalid_get_lead_batch`, then retrieve owned contacts with
`fairvalid_get_leads`. The six FairMatch tools passed controlled production sandbox acceptance;
discover actual server capabilities and permissions in the connected client.

FairMatch charges four credits per newly acquired verified work email; already-
owned and unavailable contacts cost zero. Quotes reserve no credits. Preserve the
same selected API-key identity, ordered IDs, ceiling and idempotency key after an
uncertain unlock. Do not make new paid batches to conceal uncertainty.

`leads:read` and `leads:acquire` are separate opt-in permissions. Updating a package
does not expand existing keys or OAuth grants. Deliberately reconnect with an
appropriately scoped key and review the requested permissions and cap. Installation
does not authorize acquisition. Synthetic tests require a separate direct Test-key
connection; OAuth is Live-only. See the [API/MCP guide](https://github.com/moonlitnayeem/fairvalid-ai/blob/main/docs/fairmatch.md) for
exact inputs, fixture behavior, scope boundaries and release limits.

Fresh OAuth requests in `mcp.json` include `read`, `submit`, `balance`,
`leads:read`, `leads:acquire` and `offline_access` through documented `baseScopes`.
The user must approve these permissions on FairValid. Existing grants do not
gain scopes during refresh; reconnect deliberately to enable FairMatch.
