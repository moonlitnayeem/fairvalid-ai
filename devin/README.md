![FairValid](assets/fairvalid-icon-512.png)

# FairValid for Devin

Find business leads with **FairMatch by FairValid**, quote selected contacts,
unlock verified work emails after confirming a credit ceiling, and read existing
email-verification jobs, results and credits.

Publisher: **FairValid** · Support: [nayeem@fairvalid.com](mailto:nayeem@fairvalid.com)

This candidate uses the FairValid 1.1 integration contract and Devin's native
plugin format. It contains a remote MCP declaration, the FairValid brand mark,
and three skills. It includes no executable, hook, dependency installer,
credential or account-specific configuration.

## Installation and connection

The public marketplace submission and native acceptance are pending. This
repository directory is a candidate; it does not establish availability in the
Devin marketplace.

For a reviewed local candidate, Devin supports:

```sh
devin plugins install --local /absolute/path/to/fairvalid-ai/devin
```

In Devin Cloud, open **Customize → Plugins → Add plugin → Upload .zip** and
choose the reviewed archive at Personal scope. Install the plugin, start a new
session and use `/fairvalid:fairmatch-setup` for setup guidance. That skill uses
packaged public documentation and makes no MCP calls or account connection.

For connected use, open FairValid's MCP under **Customize → MCPs** and choose
**Connect**, or use the CLI's normal `devin mcp login` flow for the installed
server. Complete browser sign-in and consent on FairValid. Select an existing
Live key for the intended workspace with suitable permissions and a credit cap.
Never paste a key, password or token into chat. The endpoint is
`https://mcp.fairvalid.com/mcp`; the transport is Streamable HTTP.

The manifest requests `read`, `balance`, `leads:read`, `leads:acquire` and
`offline_access`. It deliberately omits `submit`, covering the six FairMatch
operations and three verification reads. The hosted server may still advertise
all twelve tools; this is an OAuth permission boundary, not a native tool-list
filter. Verify the actual requested scopes before approving consent. The
candidate's native OAuth interpretation remains to be tested.

An existing key or grant does not gain permissions when a plugin is installed
or updated. Use deliberate reconnect/consent when adding FairMatch. Preserve
Devin's normal tool approval prompts. Organization or enterprise installations
have separate connection-sharing rules; use the intended account and scope.

## FairMatch workflow

Use `fairvalid_get_lead_filters`, `fairvalid_search_leads` and
`fairvalid_quote_leads` to discover and quote the user's exact selection. Before
`fairvalid_unlock_leads`, obtain explicit selection and numerical credit-ceiling
confirmation. Preserve the same idempotency key and input if a response is
uncertain. Follow `fairvalid_get_lead_batch`, then retrieve owned contacts with
`fairvalid_get_leads`.

New verified work emails cost four credits each. Already-owned and unavailable
contacts cost zero; quotes reserve no credits. The API permits 1–50 selection
IDs and a ceiling of 0–200 credits per unlock, subject to the balance and key's
lifetime cap. Search, installation and quotes authorize no acquisition or spend.

The [FairMatch skill](skills/fairmatch-leads/SKILL.md) carries the complete
permission, confirmation, retry and result-handling workflow. The
[verification-results skill](skills/verification-results/SKILL.md) reads existing
jobs and balances without submitting or cancelling work.

## Review and acceptance

Devin's contributor guide requires installation of the exact candidate and a
native session that uses a tool **or a skill** before opening a marketplace PR.
The public-docs `/fairvalid:fairmatch-setup` skill supports that bounded check
without any FairValid account grant or data access. A successful setup response
qualifies only native package/skill loading; it does not prove OAuth or FairMatch
tool execution. Do not describe those outcomes as tested until separately
observed.

Public distribution uses a reviewed, full commit SHA and `path: "devin"` in
the [official Devin marketplace](https://github.com/CognitionAI/devin-marketplace).
Provider review, merge, public discovery, installation and connected tool use are
separate steps.

[FairValid MCP guide](https://fairvalid.com/help/mcp) ·
[Privacy](https://fairvalid.com/privacy) · [Terms](https://fairvalid.com/terms) ·
[MIT License](LICENSE)

Official references: [plugin format](https://docs.devin.ai/cli/extensibility/plugins/overview),
[installation and connections](https://docs.devin.ai/product-guides/plugins),
[contributor guide](https://github.com/CognitionAI/devin-marketplace/blob/main/.agents/skills/adding-a-plugin/SKILL.md).
