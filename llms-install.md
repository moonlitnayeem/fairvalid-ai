# Install FairValid without exposing credentials

This is a remote MCP integration. No package installation, local server process,
build step, or runtime dependency is required for the FairValid server.

1. Inspect the requesting client's supported MCP configuration format. Use the
   matching example in `examples/`; do not copy another client's schema blindly.
2. Merge a server named `fairvalid` pointing to
   `https://mcp.fairvalid.com/mcp` using Streamable HTTP. Preserve existing servers
   and ask before replacing an existing FairValid connection.
3. Retain tool approval prompts. Do not add global trust, auto-approval, hooks,
   shell helpers, or permission bypasses to make installation succeed.
4. Complete OAuth in the client's browser flow. Sign-in and consent belong on
   `https://fairvalid.com`. The user selects an existing Live API key and workspace.
   Do not request credentials, consent codes, or tokens in chat or tool arguments.
5. With permission to check the connection, discover the tools and use
   `fairvalid_get_balance` with balance scope. This spends no verification credits.
   Do not submit customer addresses or cancel existing jobs as a connection test.
6. If sandbox testing is requested, use a separate direct Test-key connection
   configured in the client's protected credential mechanism. OAuth selects Live
   keys, so do not treat an OAuth connection as a sandbox. Use only documented
   reserved `example.com` fixtures, with a stable idempotency key.

If authentication or client support is unavailable, report the exact failed
operation. Do not weaken the connection to an unauthenticated endpoint or send
credentials elsewhere. A configured server is not evidence of a working tool
call. Record native client results only after performing them.

Read `skills/email-verification/SKILL.md` for credits, result interpretation,
idempotency, and cancellation behavior. Current setup help is available at
https://fairvalid.com/help/mcp. Support: nayeem@fairvalid.com.

For FairMatch lead requests, read `skills/fairmatch-leads/SKILL.md`. Version 1.1.0
adds six tools with controlled production sandbox acceptance. Existing connections keep their
permissions; lead use needs deliberate native reauthorization for `leads:read`
and, when acquisition is wanted, `leads:acquire`. OpenClaw and Hermes expose all
six FairMatch tools by default, alongside the three verification reads. Tool
availability and connection tests never authorize unlocking contacts. Get a quote and confirm the exact
numerical credit ceiling before unlock; four credits apply to each newly acquired
verified work email. Use synthetic FairMatch fixtures only in Test-key mode.
