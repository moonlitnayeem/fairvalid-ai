![FairValid](assets/fairvalid-icon-512.png)

# FairValid for Claude

> **FairValid 1.1.0:** FairMatch API/MCP passed controlled production sandbox
> acceptance on November 6, 2026. Provider listings and native-client acceptance
> are tracked separately. Discover the connected server capabilities before use;
> acquisition requires an explicit numerical credit limit and confirmation.


Verify email addresses, follow verification jobs, and review results and credit
balances in your FairValid workspace. This plugin connects Claude to FairValid's
hosted MCP server and includes separate email-verification and FairMatch skills.

**Server:** `https://mcp.fairvalid.com/mcp`

**Transport:** Streamable HTTP

**Publisher:** FairValid

**Support:** [nayeem@fairvalid.com](mailto:nayeem@fairvalid.com)

**Documentation:** [FairValid MCP guide](https://fairvalid.com/help/mcp)

## Connect your workspace

Complete OAuth on [FairValid](https://fairvalid.com), then select an existing Live
API key for the intended workspace. The selected key's scopes and lifetime
spending cap apply. A workspace Owner or Manager can manage keys on the
[API keys page](https://fairvalid.com/integrations/api-keys). Revoking the selected
key ends its connections.

Never paste a password, API key, OAuth code, or token into chat. No client secret
is bundled or required for automatic public client registration. OAuth selects
Live keys; sandbox verification needs a separate direct Test-key connection.

For Claude Code 2.1.275 or later, install this package inside a session with:

```text
/plugin install fairvalid --marketplace moonlitnayeem/fairvalid-ai
```

For older versions, first run
`/plugin marketplace add moonlitnayeem/fairvalid-ai`, then
`/plugin install fairvalid@fairvalid`. These forms follow the
[official installation reference](https://code.claude.com/docs/en/discover-plugins#add-a-marketplace-and-install-in-one-command).
The marketplace points to this dedicated `claude/` package.

To review a local checkout in Claude Code, load this dedicated folder:

```sh
claude --plugin-dir /path/to/fairvalid-ai/claude
```

Review Claude's trust prompts and complete OAuth before using the tools. Local
validation does not establish directory approval or native OAuth acceptance.

## Email-verification tools

- `fairvalid_verify_email`: submit one email address.
- `fairvalid_submit_job`: submit 1 to 5,000 email addresses.
- `fairvalid_get_job`: read job status and summary.
- `fairvalid_get_results`: read results, with up to 50 results per page.
- `fairvalid_cancel_job`: cancel remaining job work.
- `fairvalid_get_balance`: read live workspace credits.

Only submit addresses the user intends to verify and is authorized to process.
A connection or installation request does not authorize customer verification or
job cancellation. For an authorized connection check, discover the tools and
read the balance; that read spends no verification credits.

## Credits, retries, and results

Live submissions can reserve credits and return an asynchronous job. Completed
Valid and Invalid checks use one credit each. Genuine Unknown, unresolved
catch-all, technical failures, and unprocessed items have no net verification
charge. Cancellation does not reverse charges for completed checks; in-flight
work may still finish. A spending cap does not add workspace credits.

Both submission tools require a stable `idempotency_key`. If a response is
uncertain, keep the same selected API-key identity, same idempotency key, and
unchanged input. Switching credentials or retrying with a new key can create
another run. Poll accepted jobs with backoff, honor retry hints, and follow the
results cursor unchanged until all pages have been read.

An accepted job is not a completed result. Keep pending and unprocessed items
distinct from final results. Unknown and unresolved catch-all outcomes do not
prove validity; Valid does not guarantee inbox delivery. Use the shared skill
for the complete workflow and safeguards.

Default submission tests use a separate direct Test-key connection and documented
`example.com` fixtures. Sandbox work makes no live provider call and spends no
verification credits; Test keys cannot read the live balance.

A controlled live acceptance test requires the workspace owner's explicit
authorization. Stay within the authorized test addresses, workspace, selected
Live key, and credit limit; live charges and idempotency safeguards still apply.
Do not run live tests automatically, use customer lists as installation fixtures,
or cancel customer jobs as part of installation tests.

## Privacy and support

When a tool is invoked, Claude sends the supplied addresses, job identifiers,
and other tool arguments to FairValid. FairValid processes them under its
[Privacy Policy](https://fairvalid.com/privacy) and
[Terms of Service](https://fairvalid.com/terms). Anthropic also processes
conversation and tool data under its own terms. Review those policies before
connecting. For support or data-handling questions, contact
[nayeem@fairvalid.com](mailto:nayeem@fairvalid.com).

## License and brand

The plugin contains a manifest, remote MCP configuration, workflow skills, documentation,
and the FairValid icon. It defines no local executable, dependency installation,
or hooks, and bundles no credentials.

The distribution uses the [MIT License](LICENSE). FairValid names and logos
identify the publisher and remain trademarks. See the [brand guidance](BRAND.md).

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
