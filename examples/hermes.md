# FairValid in Hermes Agent (Nous Research)

Hermes supports FairValid through a remote MCP connection and the shared Agent
Skill. No native Python plugin, local server, or extra runtime is required.

For an authorized installation, Hermes' supported interactive command is:

```sh
hermes mcp add fairvalid --url https://mcp.fairvalid.com/mcp --auth oauth
```

Follow Hermes' authorization prompt to sign in at `https://fairvalid.com`, select
an existing Live API key and workspace, and review permissions. No OAuth client
secret or API key is needed in chat. FairValid supports automatic public client
registration and S256 PKCE. The selected key's workspace, scopes and cap apply.

An equivalent read-only starting configuration is in [hermes.yaml](hermes.yaml).
Merge its `fairvalid` entry into the active Hermes profile's `mcp_servers` map;
preserve existing connections. If FairValid already exists, review it before
replacing it. Hermes uses `url` and `auth: oauth`, without a transport `type` in
user configuration. The catalog manifest uses a different schema.

The tool filter limits exposure, not OAuth scopes. Review the grant at FairValid
consent. Select `fairvalid_get_balance`, `fairvalid_get_job`, and `fairvalid_get_results`
for initial use. Only enable `fairvalid_verify_email`, `fairvalid_submit_job`, and
`fairvalid_cancel_job` when those actions are wanted. Review the selection through
`hermes mcp configure fairvalid`. To reconnect an existing OAuth server, use
`hermes mcp login fairvalid`. Start a fresh session or use `/reload-mcp` after setup.

`hermes mcp test fairvalid` connects and discovers tools. It is not proof that an
authenticated business operation succeeded. For an authorized functional check,
ask Hermes to read the FairValid balance only, with balance scope. This spends
no verification credits. Do not submit customer addresses or cancel customer jobs
as an installation test. OAuth connections use Live keys; sandbox submissions
need a separate direct Test-key connection and documented `example.com` fixtures.

The skill can be inspected and installed independently:

```sh
hermes skills inspect moonlitnayeem/fairvalid-ai/skills/email-verification
hermes skills install moonlitnayeem/fairvalid-ai/skills/email-verification
```

Review the skill and Hermes' normal scan and confirmation. Do not bypass scanning
with `--force`. Installing the skill does not create an MCP connection or grant
account access. The GitHub skill is a community-source install in Hermes; it is
not a Nous-approved catalog listing.

Hermes also accepts a public repository as a custom skill tap. That is a user
subscription to the source, not approval or guaranteed inclusion in global search.
The official MCP catalog has a separate maintainer-reviewed contribution route
under `optional-mcps/` in the NousResearch/hermes-agent repository.

Read-only local checks on 30 October 2026 found Hermes Agent v0.22.5
(2026.9.24), revision `bf0203a794a0`, with the documented MCP OAuth and skill
commands. No host integration, private configuration, credentials, OAuth grant,
or native FairValid tool call was inspected or changed for those checks.

Sources:

- [Official Hermes MCP guide and catalog contribution route](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)
- [Official connection-test semantics](https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes)
- [Official Skills System and GitHub tap support](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
- [FairValid MCP documentation](https://fairvalid.com/help/mcp)
