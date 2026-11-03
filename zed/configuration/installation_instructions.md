# Connect FairValid

FairValid verifies email addresses and exposes job status, results, cancellation and credit-balance tools through its hosted MCP server.

This extension uses the pinned `mcp-remote` 0.16.0 bridge and requires a compatible Node.js runtime (20.18.1 is the declared dependency baseline; resolved dependencies may require newer). Zed obtains Node and installs the bridge through its extension API. Connecting can open your browser for normal FairValid OAuth consent.

Sign in to FairValid and select the intended workspace and an existing active Live API key with the requested permissions. The selected key's scopes and spending cap apply. An Owner or Manager can manage keys at https://fairvalid.com/integrations/api-keys. Never paste a password, key, authorization code or token into chat or extension settings.

If first-time sign-in exceeds Zed's default 60-second timeout, restart FairValid from MCP settings and use the current authorization flow. If needed, set the top-level Zed setting `"context_server_timeout": 300` before restarting; it affects context-server requests generally. Do not keep using an authorization callback from a stopped bridge.

A chat-driven tool call also requires an available model provider in Zed. If the Agent Panel reports **Permission Denied — Trial access is blocked**, resolve Zed/model-provider access before retrying. The local development check completed installation, OAuth and discovery of all six tools, but its balance request was blocked before tool execution.

Start with “Show my FairValid credit balance.” This read does not spend verification credits. Only request verification or cancellation when you intend that operation. Verification can reserve credits and complete asynchronously; inconclusive results do not prove an address is deliverable. Follow the job status and results before making a claim about completion or cost.

OAuth files are kept under `fairvalid-oauth` in Zed's designated extension work directory, separately from your project and from other `mcp-remote` clients. This storage separation is not a process sandbox. Revoking the backing FairValid key ends its connections; uninstalling an extension alone is not evidence that server-side authorization was revoked.

Documentation: https://fairvalid.com/help/mcp
Publisher and support: FairValid · nayeem@fairvalid.com
