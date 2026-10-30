# Client configuration examples

These files contain connection metadata, not credentials. Merge only the relevant
server entry into the client's configuration and preserve existing entries.
Review its trust and OAuth prompts. OAuth signs in on `https://fairvalid.com`
and selects an existing Live API key; no client secret is bundled.

| Client | Example | Setup surface |
| --- | --- | --- |
| Claude Code | [claude-code.json](claude-code.json) | Project `.mcp.json` or the client MCP setup command |
| Cursor | [cursor.json](cursor.json) | Cursor MCP configuration; the plugin already supplies this |
| Gemini CLI | [gemini.json](gemini.json) | `mcpServers` in Gemini settings; the extension already supplies this |
| Cline | [cline.json](cline.json) | MCP Servers → Configure MCP Servers, or Remote Servers → Streamable HTTP |
| Grok Build | [grok.toml](grok.toml) | The `mcp_servers` section of Grok configuration |
| VS Code | [vscode.json](vscode.json) | Workspace `.vscode/mcp.json`, or MCP: Add Server → HTTP |
| GitHub Copilot | [copilot.json](copilot.json) | Workspace `.mcp.json` or user `mcp-config.json` |
| Hermes Agent (Nous Research) | [OAuth YAML and commands](#hermes-agent-nous-research) | Active profile `mcp_servers` configuration |

Claude web/Desktop can connect through **Customize → Connectors → Add custom
connector** using the endpoint directly. This is different from installing a
Claude Code plugin. Grok Build's marketplace is also separate from a grok.com
custom connector. Provider availability and organization policies can differ.

Use the client's browser authorization flow. For an authorized connection test,
discover all six FairValid tools and call `fairvalid_get_balance` with balance
scope. This is a read and uses no verification credits. Do not run live
verification or cancel customer jobs just to test installation.

For sandbox submissions, create a separate direct Test-key connection through
the client's protected credential settings and use documented `example.com`
fixtures. These OAuth examples are Live-key connections. Do not put real keys
into these files or paste them in chat.

Configuration schemas were checked against the official documentation below on
30 October 2026. This is not an assertion that each native client was installed
or successfully exercised.

- [Claude Code MCP](https://code.claude.com/docs/en/mcp)
- [Claude manifest reference](https://code.claude.com/docs/en/plugins-reference)
- [Cursor plugins reference](https://cursor.com/docs/reference/plugins)
- [Cursor MCP](https://cursor.com/docs/mcp)
- [Gemini MCP and OAuth](https://geminicli.com/docs/tools/mcp-server/)
- [Gemini extension reference](https://geminicli.com/docs/extensions/reference/)
- [Cline MCP](https://docs.cline.bot/mcp/mcp-overview)
- [Grok Build MCP](https://docs.x.ai/build/features/mcp-servers)
- [Grok plugin compatibility](https://docs.x.ai/build/features/skills-plugins-marketplaces)
- [VS Code and portable Copilot MCP configuration](https://code.visualstudio.com/docs/agents/reference/mcp-configuration)

Notable schema differences: Claude Code requires `type: "http"`; Cursor infers
HTTP from `url`; Gemini requires `httpUrl` for Streamable HTTP (`url` denotes
SSE); Cline uses `type: "streamableHttp"`; VS Code uses a `servers` wrapper;
Grok uses TOML `mcp_servers`.


## Hermes Agent (Nous Research)

Hermes connects to the hosted endpoint through native MCP OAuth. For an
installation you want to perform, use its interactive setup:

```sh
hermes mcp add fairvalid --url https://mcp.fairvalid.com/mcp --auth oauth
```

Complete sign-in and consent at `https://fairvalid.com`, choosing the intended
workspace and existing Live API key. No client secret is needed. An equivalent
starting configuration limits the visible tools to reads:

```yaml
mcp_servers:
  fairvalid:
    url: https://mcp.fairvalid.com/mcp
    auth: oauth
    tools:
      include:
        - fairvalid_get_balance
        - fairvalid_get_job
        - fairvalid_get_results
```

The tool filter limits exposure, not OAuth scopes. Review the grant at FairValid
consent. Merge this into the active Hermes profile's `mcp_servers` map and preserve other
connections. Review an existing FairValid entry before changing it. Use
`hermes mcp configure fairvalid` to enable submission or cancellation only when
wanted. `hermes mcp login fairvalid` reauthorizes an existing OAuth connection;
restart the session or use `/reload-mcp` after setup.

`hermes mcp test fairvalid` checks connection and tool discovery. For an authorized
functional check, ask for the FairValid balance only; this spends no verification
credits. Discovery alone does not prove a successful authenticated tool call.
Do not submit customer addresses or cancel customer jobs to test installation.
OAuth uses Live keys; sandbox work requires a separate direct Test-key connection.

The shared skill is independently available through GitHub:

```sh
hermes skills inspect moonlitnayeem/fairvalid-ai/skills/email-verification
hermes skills install moonlitnayeem/fairvalid-ai/skills/email-verification
```

Keep Hermes' security scan and confirmation; do not use `--force` to bypass them.
A skill installation supplies instructions, without creating a connection or
account grant. This public GitHub skill is a community-source install in Hermes.
Official MCP catalog inclusion requires a separate accepted PR to
`NousResearch/hermes-agent/optional-mcps/`.

Read-only checks on 30 October 2026 confirmed these command forms in the installed
Hermes Agent v0.22.5 (2026.9.24), revision `bf0203a794a0`. No native FairValid OAuth
connection or authenticated tool call was performed for that check.

References: [Hermes MCP and catalog contribution](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp),
[connection tests](https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes),
and [skills and public GitHub taps](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills).
