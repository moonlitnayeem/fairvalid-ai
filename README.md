![FairValid](assets/fairvalid-icon-512.png)

# FairValid for AI assistants

> **FairValid 1.1.0:** FairMatch API/MCP passed controlled production sandbox
> acceptance on November 6, 2026. Provider listings and native-client acceptance
> are tracked separately. Discover the connected server capabilities before use;
> acquisition requires an explicit numerical credit limit and confirmation.


Verify email addresses and use **FairMatch by FairValid** to find business leads,
quote selected contacts, and unlock verified work emails with a confirmed credit
ceiling. This package connects to FairValid's hosted Model Context Protocol (MCP)
server and includes separate verification and FairMatch workflow skills.

**Server:** `https://mcp.fairvalid.com/mcp`  
**Transport:** Streamable HTTP  
**Publisher and support:** FairValid · [nayeem@fairvalid.com](mailto:nayeem@fairvalid.com)  
**Documentation:** [fairvalid.com/help/mcp](https://fairvalid.com/help/mcp)

## Connect your workspace

Use OAuth in a supported client. Sign in and approve access on
[FairValid](https://fairvalid.com), then select an existing Live API key covering
the requested permissions. Its workspace, scopes, and lifetime spending cap apply
to the connection. A workspace Owner or Manager can manage keys on the
[API keys page](https://fairvalid.com/integrations/api-keys). Revoking the selected
key ends its connections.

FairMatch adds opt-in `leads:read` and `leads:acquire` permissions. Existing keys
and grants keep their existing permissions; a package update cannot expand them.
To enable FairMatch, deliberately reconnect through native OAuth and select an
appropriately scoped key. Review the new permissions and cap before consent.
OpenAI 1.1.0 requests both lead scopes during fresh authorization. OpenClaw and
Hermes include all six FairMatch tools alongside the three verification reads.
Their filters do not grant OAuth permissions or authorize spending: unlock still
requires `leads:acquire`, a quote and explicit approval of a numerical maximum.

No client secret is bundled or required for automatic public client registration.
Never paste a key, password, OAuth code, or token into chat. For a client that
uses bearer headers, configure an existing key through its protected credential
settings. A direct Test key can be used for sandbox fixtures; OAuth currently
selects Live keys.

## Supported package formats

| Client | Included configuration |
| --- | --- |
| Claude / Claude Code | Dedicated plugin package in [claude](claude/README.md) |
| ChatGPT / Codex | Separate portable plugin package in [openai](openai/README.md) |
| Grok Build | Claude-compatible plugin and MCP files, plus the shared skill |
| Cursor | `.cursor-plugin/plugin.json`, `mcp.json`, and shared skill |
| Gemini CLI | Root `gemini-extension.json` and shared skill |
| Hermes Agent (Nous Research) | Native HTTP OAuth setup and shared skill in [examples](examples/README.md) |
| OpenClaw | Claude-format bundle with [marketplace installation and native sign-in](#openclaw-marketplace-installation) |
| Zed | Local transport extension and connection instructions in [zed](zed/README.md) |
| Other MCP clients | Provider-specific configurations in [examples](examples/README.md) |

Package configuration does not establish a marketplace listing or prove a
successful connection in every client. Provider account access, permissions,
review, and native client acceptance are separate steps.

For Claude Code 2.1.275 or later, install inside a session with
`/plugin install fairvalid --marketplace moonlitnayeem/fairvalid-ai`.
For older versions, use `/plugin marketplace add moonlitnayeem/fairvalid-ai`
followed by `/plugin install fairvalid@fairvalid`.
These forms follow the [official installation reference](https://code.claude.com/docs/en/discover-plugins#add-a-marketplace-and-install-in-one-command).
The marketplace installs the dedicated `claude/` package. A maintainer can
validate that folder with
`claude plugin validate /path/to/fairvalid-ai/claude --strict --profile directory`.
Users can review and load a local public checkout with
`claude --plugin-dir /path/to/fairvalid-ai/claude`.
For Gemini CLI, the public repository can be installed with
`gemini extensions install https://github.com/moonlitnayeem/fairvalid-ai`.
These commands require that the referenced checkout or published repository exists.
Review client trust prompts and complete OAuth before using the tools.

### OpenClaw marketplace installation

FairValid **1.1.0** is published on
[ClawHub](https://clawhub.ai/fairvalid/plugins/fairvalid). Install and enable the
FairValid plugin, then open **Plugins → FairValid → Accounts** in your OpenClaw
Gateway. Choose **Connect** beside `fairvalid` and complete the FairValid browser
consent. Select your workspace and a Live API key covering the requested
permissions and an appropriate lifetime spending cap.

Start a new agent session and ask “Show my FairValid credit balance.” For
FairMatch, ask to search and quote leads before approving an exact selection and
numerical credit ceiling. The published bundle exposes all six FairMatch tools
and three verification read tools. Existing connections need deliberate consent
for the lead permissions.

On November 6, 2026, all six FairMatch tools passed a live end-to-end test through
the installed ClawHub 1.1.0 bundle on OpenClaw 2026.11.1, using its native Claude
CLI runtime with Claude Code 2.1.312. The test retrieved an existing owned contact
through a confirmed zero-credit batch, with no additional acquisition charge.

## What you can do

| Tool | Purpose | Permission |
| --- | --- | --- |
| `fairvalid_verify_email` | Submit one address for verification | `submit` |
| `fairvalid_submit_job` | Submit a batch of 1 to 5,000 addresses | `submit` |
| `fairvalid_get_job` | Read a job's status and summary | `read` |
| `fairvalid_get_results` | Read up to 50 results per page | `read` |
| `fairvalid_cancel_job` | Cancel remaining job work | `submit` |
| `fairvalid_get_balance` | Read live workspace credits | `balance` |
| `fairvalid_get_lead_filters` | Discover FairMatch filter keys, choices and limits | `leads:read` |
| `fairvalid_search_leads` | Preview up to 50 matching people; no paid unlock | `leads:read` |
| `fairvalid_quote_leads` | Quote 1–50 selected people without reserving credits | `leads:read` |
| `fairvalid_unlock_leads` | Start a confirmed acquisition batch with a credit ceiling | `leads:acquire` |
| `fairvalid_get_lead_batch` | Read the same key's acquisition batch and charges | `leads:read` |
| `fairvalid_get_leads` | Read up to 100 owned verified contacts per page | `leads:read` |

Examples of requests:

- “Show my FairValid credit balance.”
- “Show the current status and results for this FairValid job.”
- “Verify these email addresses with FairValid.”
- “Find FairMatch leads matching my criteria, then show a quote before unlocking.”
- “Show my saved FairMatch leads without acquiring any new contacts.”

The verification request starts live work when connected through OAuth or a Live key.
Only submit addresses you intend to verify and are authorized to process.

## Credits and result interpretation

Live submissions can reserve credits and return an asynchronous job. Completed
Valid and Invalid checks use one credit each. Genuine Unknown, unresolved
catch-all, technical failures, and unprocessed items have no net verification
charge. Cancellation does not reverse charges for completed checks; in-flight
work may still finish. A spending cap does not add credits to a workspace.

An accepted job is not a completed result. Poll with backoff, honor retry hints,
and follow the results cursor to read all pages. Keep pending and unprocessed
items distinct from final results. Unknown or unresolved catch-all is not proof
of validity; Valid is not a guarantee of inbox delivery.

Both submission tools require a stable `idempotency_key`. On an uncertain
response, keep the **same selected API-key identity, same key, and unchanged
input**. Reconnecting to a different API key can create another run even if the
idempotency key is unchanged. Do not rotate keys or resubmit with a new key just
to make an uncertain request appear successful.

## FairMatch selection, credits and confirmation

FairMatch follows **search → quote → explicit maximum-credit confirmation →
unlock → poll batch → retrieve owned leads**. Four credits are charged for each
newly acquired verified work email; already-owned and unavailable contacts cost
zero. A quote reserves no credits and does not guarantee a deliverable contact.
Unlock accepts 1–50 distinct selection IDs, `maximumCredits` from 0–200,
`confirm: true`, and a stable `idempotency_key`. Only set confirmation after the
user approves that exact selection and numerical ceiling. Do not split work to
bypass the ceiling, workspace balance or key's shared lifetime cap.

Live selections expire after 30 minutes. If admission is uncertain, reuse the
original IDs, ceiling, idempotency key and API-key identity; do not refresh the
selection or make another paid batch to hide uncertainty. Accepted batches can
remain `working`; follow `batch_id` and report observed `charged_credits` after
processing. Lead ownership does not authorize outreach.

See the [FairMatch API/MCP guide](docs/fairmatch.md) for exact argument fields,
permission upgrades, synthetic test cases and release limits, and the
[FairMatch skill](skills/fairmatch-leads/SKILL.md) for the complete workflow.

## Connection and acceptance tests

A connection or installation request does not authorize customer verification or
job cancellation or lead acquisition. For an authorized OAuth connection check,
discover the currently available tools and call `fairvalid_get_balance`; that read spends no verification credits.

Default submission tests use a separate direct Test-key connection and the
documented `example.com` fixtures. Sandbox work makes no live provider call and
spends no verification credits; Test keys cannot read the live balance.

A controlled live acceptance test requires the workspace owner's explicit
authorization. Stay within the authorized test addresses, workspace, selected
Live key, and credit limit; live charges and idempotency safeguards still apply.
Do not run live tests automatically, use customer lists as installation fixtures,
or cancel customer jobs as part of installation tests.

The packages contain manifests, the workflow skill, examples, and brand assets.
The optional [Zed extension](zed/README.md) also downloads and runs a pinned local
transport bridge and stores OAuth credentials in its extension work directory.
No credentials are bundled. Client validation, live protocol checks, and native
client tests must each be recorded according to what was actually performed;
none implies a provider's approval or publication. See the
[static validation record](VALIDATION.md).

## Privacy policy

When you invoke a tool, the connected AI provider sends the supplied addresses,
job and lead identifiers, search criteria, and other tool arguments to FairValid.
FairMatch can return owned business-contact data to the connected assistant. FairValid processes them
under its [Privacy Policy](https://fairvalid.com/privacy) and
[Terms](https://fairvalid.com/terms). The AI provider also processes conversation
and tool data under its own terms. Review those policies before connecting.
The packages add no analytics. The Zed extension's local OAuth storage is described
in its [connection instructions](zed/README.md#local-oauth-storage).
For support or data-handling questions, contact
[nayeem@fairvalid.com](mailto:nayeem@fairvalid.com).

## License and brand

The distribution code, manifests, and documentation are available under the
[MIT License](LICENSE). FairValid names and logos identify the publisher and do
not grant trademark rights or permission to imply endorsement of another service.
See [brand guidance](assets/BRAND.md).
