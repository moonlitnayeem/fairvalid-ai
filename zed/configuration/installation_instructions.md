# Connect FairValid

FairValid verifies email addresses and exposes job status, results, cancellation and credit-balance tools through its hosted MCP server.

This extension uses the pinned `mcp-remote` 0.16.0 bridge and requires a compatible Node.js runtime (20.18.1 is the declared dependency baseline; resolved dependencies may require newer). Zed obtains Node and installs the bridge through its extension API. Connecting can open your browser for normal FairValid OAuth consent.

Sign in to FairValid and select the intended workspace and an existing active Live API key with the requested permissions. The selected key's scopes and spending cap apply. An Owner or Manager can manage keys at https://fairvalid.com/integrations/api-keys. Never paste a password, key, authorization code or token into chat or extension settings.

If first-time sign-in exceeds Zed's default 60-second timeout, restart FairValid from MCP settings and use the current authorization flow. If needed, set the top-level Zed setting `"context_server_timeout": 300` before restarting; it affects context-server requests generally. Do not keep using an authorization callback from a stopped bridge.

A chat-driven tool call also requires an available model provider in Zed. If the Agent Panel reports **Permission Denied — Trial access is blocked**, resolve Zed/model-provider access before retrying. The earlier 0.1.0 development check completed installation, OAuth and discovery of the six verification tools, but its balance request was blocked before tool execution. It did not test FairMatch or this 1.1.0 package.

Start with “Show my FairValid credit balance.” This read does not spend verification credits. Only request verification or cancellation when you intend that operation. Verification can reserve credits and complete asynchronously; inconclusive results do not prove an address is deliverable. Follow the job status and results before making a claim about completion or cost.

OAuth files are kept under `fairvalid-oauth` in Zed's designated extension work directory, separately from your project and from other `mcp-remote` clients. This storage separation is not a process sandbox. Revoking the backing FairValid key ends its connections; uninstalling an extension alone is not evidence that server-side authorization was revoked.

Documentation: https://fairvalid.com/help/mcp
Publisher and support: FairValid · nayeem@fairvalid.com

## FairMatch lead workflows — 1.1.0

FairMatch adds filter discovery, business-lead search, quotes, confirmed unlocks,
batch status and owned-lead retrieval. The server passed controlled production
sandbox acceptance on November 6, 2026; native Zed FairMatch execution remains
unverified.
Discover actual tool schemas; do not assume absent tools are live. Existing OAuth
grants retain existing scopes. Deliberately reconnect with an appropriately scoped
key for `leads:read` and, when acquisition is wanted, `leads:acquire`. Never modify
stored tokens or bypass a scope denial.

Use `fairvalid_get_lead_filters`, then `fairvalid_search_leads` for the user's
criteria. Quote 1–50 distinct returned selection IDs using `fairvalid_quote_leads`;
quotes reserve no credits. Explain four credits per newly acquired verified work
email and zero for already-owned/unavailable contacts. Obtain explicit approval
of the exact selection and numerical maximum before `fairvalid_unlock_leads`.
Pass the approved `maximumCredits` (0–200), `confirm: true` and one stable
`idempotency_key` (8–128 allowed characters). Never unlock on installation alone.

On uncertain admission retain the same API-key identity, ordered IDs, ceiling
and idempotency key. Durable replay is checked before the live selection's
30-minute expiry; do not silently replace IDs on retries. Follow the actual
`batch_id` with `fairvalid_get_lead_batch`, honor retry hints and back off from
5 to 30 seconds. Report observed status/charges rather than assuming completion.
`fairvalid_get_leads` retrieves up to 100 owned contacts per page; pass
`next_cursor` unchanged as `cursor`. Contact ownership does not authorize outreach.

Sandbox tests require a separate direct Test-key connection and documented
synthetic FairMatch fixtures; OAuth is Live-only. No native FairMatch acceptance
is established by this package. Support: nayeem@fairvalid.com.
