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
