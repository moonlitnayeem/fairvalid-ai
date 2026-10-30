![FairValid](assets/icon.png)

# FairValid for OpenClaw

Use FairValid from OpenClaw to inspect email verification jobs, read results,
check workspace credits, and verify user-selected addresses when submission is
enabled. Publisher: FairValid. Support: nayeem@fairvalid.com.

This is a Claude-format bundle recognized by OpenClaw: one bundle manifest, a
remote MCP declaration, and a workflow skill. It includes no local runtime,
executable, hook, dependency installer, credential, or telemetry integration.

The server is `https://mcp.fairvalid.com/mcp`, using Streamable HTTP and OAuth.
Review the bundle, then use OpenClaw's normal plugin installation flow. A local
reviewed directory can be installed with `openclaw plugins install <directory>`.
A registry install command can be provided after ClawHub publishes the package;
this README does not assert that a listing exists.

Complete the FairValid sign-in and consent flow through OpenClaw. Select an
existing Live API key for the intended workspace. Its scopes and lifetime cap
apply. No client secret is required for automatic registration. Never paste
credentials or authorization codes into chat.

OpenClaw defaults native OAuth credentials to shared, operator-managed access.
Review which agents and users may use that connection. Deployments needing each
sender's own account should use OpenClaw's documented per-requester OAuth setup;
that requires a configured public Gateway origin. This bundle does not change
gateway access or invent that deployment setting.

The initial tool filter exposes `fairvalid_get_balance`, `fairvalid_get_job`, and
`fairvalid_get_results`. This limits visible tools, **not OAuth scopes**. The
complete service also offers `fairvalid_verify_email`, `fairvalid_submit_job`,
and `fairvalid_cancel_job`; enable those tools through reviewed host settings
when their actions are wanted. Preserve existing permissions and tool approval
prompts.

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
