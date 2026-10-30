![FairValid](assets/fairvalid-icon-512.png)

# FairValid for AI assistants

Verify email addresses from your AI assistant, follow verification jobs, and read
results in your FairValid workspace. This package connects to FairValid's hosted
Model Context Protocol (MCP) server and includes a skill for handling verification,
credits, retries, and result interpretation.

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

No client secret is bundled or required for automatic public client registration.
Never paste a key, password, OAuth code, or token into chat. For a client that
uses bearer headers, configure an existing key through its protected credential
settings. A direct Test key can be used for sandbox fixtures; OAuth currently
selects Live keys.

## Supported package formats

| Client | Included configuration |
| --- | --- |
| Claude / Claude Code | `.claude-plugin/plugin.json`, `.mcp.json`, and shared skill |
| ChatGPT / Codex | Separate portable plugin package in [openai](openai/README.md) |
| Grok Build | Claude-compatible plugin and MCP files, plus the shared skill |
| Cursor | `.cursor-plugin/plugin.json`, `mcp.json`, and shared skill |
| Gemini CLI | Root `gemini-extension.json` and shared skill |
| Hermes Agent (Nous Research) | Native HTTP OAuth setup and shared skill in [examples](examples/README.md) |
| OpenClaw | Separate Claude-format bundle in [openclaw](openclaw/README.md) |
| Other MCP clients | Provider-specific configurations in [examples](examples/README.md) |

Package configuration does not establish a marketplace listing or prove a
successful connection in every client. Provider account access, permissions,
review, and native client acceptance are separate steps.

For Claude Code 2.1.275 or later, install inside a session with
`/plugin install fairvalid --marketplace moonlitnayeem/fairvalid-ai`.
For older versions, use `/plugin marketplace add moonlitnayeem/fairvalid-ai`
followed by `/plugin install fairvalid@fairvalid`.
These forms follow the [official installation reference](https://code.claude.com/docs/en/discover-plugins#add-a-marketplace-and-install-in-one-command).
A maintainer can validate this folder with
`claude plugin validate /path/to/fairvalid-ai --strict`. Users can review and load
a local checkout with `claude --plugin-dir /path/to/fairvalid-ai`.
For Gemini CLI, the public repository can be installed with
`gemini extensions install https://github.com/moonlitnayeem/fairvalid-ai`.
These commands require that the referenced checkout or published repository exists.
Review client trust prompts and complete OAuth before using the tools.

## What you can do

| Tool | Purpose | Permission |
| --- | --- | --- |
| `fairvalid_verify_email` | Submit one address for verification | `submit` |
| `fairvalid_submit_job` | Submit a batch of 1 to 5,000 addresses | `submit` |
| `fairvalid_get_job` | Read a job's status and summary | `read` |
| `fairvalid_get_results` | Read up to 50 results per page | `read` |
| `fairvalid_cancel_job` | Cancel remaining job work | `submit` |
| `fairvalid_get_balance` | Read live workspace credits | `balance` |

Examples of requests:

- “Show my FairValid credit balance.”
- “Show the current status and results for this FairValid job.”
- “Verify these email addresses with FairValid.”

The last request starts live work when connected through OAuth or a Live key.
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

## Test without customer actions

Installation and connection tests must not submit customer addresses or cancel
customer jobs. For an authorized OAuth connection check, discover the six tools
and call `fairvalid_get_balance`; that read spends no verification credits.
To test submissions, use a separate direct Test-key connection and the documented
`example.com` fixtures. Sandbox work makes no live provider call and spends no
verification credits. Test keys cannot read the live balance.

This package does not install host settings, run local executables, define hooks,
or bundle credentials. It contains manifests, the workflow skill, examples, and
brand assets. Client validation, live protocol checks, and native client tests
must each be recorded according to what was actually performed; none implies a
provider's approval or publication. See the [static validation record](VALIDATION.md).

## Privacy policy

When you invoke a tool, the connected AI provider sends the supplied addresses,
job identifiers, and other tool arguments to FairValid. FairValid processes them
under its [Privacy Policy](https://fairvalid.com/privacy) and
[Terms](https://fairvalid.com/terms). The AI provider also processes conversation
and tool data under its own terms. Review those policies before connecting.
The package itself adds no analytics, local database, or extra data destination.
For support or data-handling questions, contact
[nayeem@fairvalid.com](mailto:nayeem@fairvalid.com).

## License and brand

The distribution code, manifests, and documentation are available under the
[MIT License](LICENSE). FairValid names and logos identify the publisher and do
not grant trademark rights or permission to imply endorsement of another service.
See [brand guidance](assets/BRAND.md).
