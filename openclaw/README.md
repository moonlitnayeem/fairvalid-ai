![FairValid](assets/icon.png)

# FairValid for OpenClaw

> **FairValid 1.1.0:** FairMatch API/MCP passed controlled production sandbox
> acceptance on November 6, 2026. Provider listings and native-client acceptance
> are tracked separately. Discover the connected server capabilities before use;
> acquisition requires an explicit numerical credit limit and confirmation.


Use FairValid from OpenClaw to search FairMatch leads, quote and acquire verified
work emails with a confirmed credit ceiling, inspect verification jobs, read
results and check credits. Publisher: FairValid. Support: nayeem@fairvalid.com.

This is a Claude-format bundle recognized by OpenClaw: one bundle manifest, a
remote MCP declaration, and two workflow skills. It includes no local runtime,
executable, hook, dependency installer, credential, or telemetry integration.

The server is `https://mcp.fairvalid.com/mcp`, using Streamable HTTP and OAuth.
Review the bundle, then use OpenClaw's normal plugin installation flow. A local
reviewed directory can be installed with `openclaw plugins install <directory>`.
The [FairValid listing](https://clawhub.ai/fairvalid/plugins/fairvalid) has a prior
1.0.0 release. Check the listing's actual version and publication status when
installing; repository availability and registry publication are separate.

Complete the FairValid sign-in and consent flow through OpenClaw. Select an
existing Live API key for the intended workspace. Its scopes and lifetime cap
apply. No client secret is required for automatic registration. Never paste
credentials or authorization codes into chat.

OpenClaw defaults native OAuth credentials to shared, operator-managed access.
Review which agents and users may use that connection. Deployments needing each
sender's own account should use OpenClaw's documented per-requester OAuth setup;
that requires a configured public Gateway origin. This bundle does not change
gateway access or invent that deployment setting.

The default tool filter exposes the three verification reads plus
`fairvalid_get_lead_filters`, `fairvalid_search_leads`, `fairvalid_quote_leads`,
`fairvalid_unlock_leads`, `fairvalid_get_lead_batch` and `fairvalid_get_leads`:
nine tools in total. This makes the complete FairMatch workflow available after
authorization; it grants neither OAuth scopes nor permission to spend credits.
Approve `leads:read` and `leads:acquire` in FairValid consent, quote the chosen
leads, and confirm the exact numerical credit ceiling before each unlock.
Preserve normal tool approval prompts. If an administrator narrows the filter,
respect that restriction. Verification submission/cancellation tools remain
opt-in host configuration.

For an authorized connection check, discover tools and read the balance with
balance scope. Reading the balance spends no verification credits. Authentication
saved, tool discovery, and a successful tool call are distinct outcomes. Do not
verify customer addresses or cancel customer jobs as an installation test.
OAuth uses Live keys; sandbox submissions require a separate direct Test-key
connection and documented `example.com` fixtures.

Live submissions create asynchronous jobs and can reserve credits. Completed
Valid and Invalid checks use one credit each. Genuine Unknown, unresolved
catch-all, technical failures, and unprocessed items have no net verification
charge. Cancellation does not reverse completed-check charges. Retry an uncertain
submission with the same selected API-key identity, idempotency key, and unchanged
input; do not create duplicate work to obtain a success response.

The shared workflow is in
[skills/fairvalid-email-verification/SKILL.md](skills/fairvalid-email-verification/SKILL.md).
It covers polling, pagination, result uncertainty, and safe retries. Valid is
not a guarantee of inbox delivery.

Tool arguments and results are processed by FairValid and the connected AI
provider under their respective policies. See
[FairValid MCP docs](https://fairvalid.com/help/mcp),
[Privacy Policy](https://fairvalid.com/privacy), and
[Terms](https://fairvalid.com/terms).

Distribution code and documentation use the [MIT License](LICENSE). FairValid
trademark rights are not granted. No native OpenClaw account authentication or
FairValid tool execution has been claimed by this package.

Official format references:
[OpenClaw bundles](https://docs.openclaw.ai/plugins/bundles),
[MCP connections](https://docs.openclaw.ai/tools/mcp), and
[OAuth transport behavior](https://docs.openclaw.ai/cli/mcp/transports).

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
