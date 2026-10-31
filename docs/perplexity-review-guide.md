# FairValid — Perplexity evaluation guide

![FairValid](https://raw.githubusercontent.com/moonlitnayeem/fairvalid-ai/main/assets/fairvalid-icon-512.png)

FairValid verifies email addresses and exposes six MCP tools for submissions,
job status, results, cancellation and workspace verification-credit balance.
Endpoint: **`https://mcp.fairvalid.com/mcp`** (Streamable HTTP).

This guide describes proposed Perplexity review cases and their expected
behavior. **Native Perplexity installation, OAuth and tool execution have not
been verified.** It is not a completed Perplexity acceptance report.

## Secure review access and roles

- Contact **[nayeem@fairvalid.com](mailto:nayeem@fairvalid.com)** to coordinate an
  isolated review workspace and an agreed review scope. No credentials are
  published here or supplied through chat, this repository or an application form.
- OAuth opens FairValid's own sign-in and consent pages. A verified workspace
  **owner or manager** selects an existing **Live API key** covering the requested
  permissions. The key determines the workspace and spending cap. Reviewers must
  use their own authorized account; do not share an owner's login.
- Start an authorized Live/OAuth connection check with `fairvalid_get_balance`
  and `balance` permission. This does not submit email checks or spend
  verification credits. A connection check does not authorize live submissions.
- Synthetic tests require a **separate direct Test-key connection** in a client
  supporting protected bearer-header configuration. Enter the Test key only in
  that client's protected credential settings. **OAuth currently selects Live
  keys; never run the fixtures below through OAuth or a Live-key connection.**
- If Perplexity does not support that direct Test-key setup, use an agreed
  compatible MCP test client for the sandbox cases. A native Perplexity live test
  requires separate owner authorization, an isolated workspace, a bounded key
  cap and reviewer-controlled addresses. A sandbox result cannot substitute for
  native Perplexity acceptance.

## Documented synthetic fixtures

Use only these reserved `example.com` fixtures after confirming Test-key mode.
Every fixture is simulated: **no verification-provider call and zero charged
credits**. For a single check, the expected values are:

| Address | `result` value | Underlying API status |
| --- | --- | --- |
| `deliverable@example.com` | `valid` | 200 |
| `undeliverable@example.com` | `invalid` | 200 |
| `risky@example.com` | `catch_all` | 200 |
| `unknown@example.com` | `unknown` | 200 |
| `pending@example.com` | `pending` | 202 |
| `error@example.com` | `error` | 503 |

Single-fixture checks return a simulated result, **not a job to poll**, including
the pending fixture. Batch fixtures create a sandbox job: its state is `pending`
if any address is the pending fixture; otherwise `failed` if any address is the
error fixture; otherwise `completed`. A new batch returns API status 202 even
when its simulated state is already completed or failed; an identical replay
returns the existing job with API status 200.
The pending batch does not automatically complete; read its state once, inspect
its results, then use the explicitly authorized cancellation case below.

## Six-tool prompt and expected-action matrix

The first five cases use the confirmed **Test-key connection**. Use the example
idempotency keys for one review run; keep each key and its exact inputs unchanged
on retries. Assign a new non-personal run prefix only for intentional new work.

| Tool / Live scope | Example reviewer prompt | Expected action and result |
| --- | --- | --- |
| `fairvalid_verify_email` / `submit` | “Using the Test-key connection, verify `deliverable@example.com` with idempotency key `perplexity-review-single-01`.” | Return simulated `valid`, zero charged credits and no provider submission; no job polling. |
| `fairvalid_submit_job` / `submit` | “Using the Test-key connection, submit `deliverable@example.com` and `undeliverable@example.com` with idempotency key `perplexity-review-batch-01`.” | Return a sandbox job ID, `completed` state and zero charged credits. Repeating the unchanged request with the same key returns the same job. |
| `fairvalid_get_job` / `read` | “Read the status of the sandbox batch just returned.” | Use that returned job ID; report the observed state without submitting another batch. |
| `fairvalid_get_results` / `read` | “Show the results of that sandbox batch.” | Return `valid` and `invalid` results, with no charge or provider submission. Respect `next_cursor` for pagination; pages contain at most 50 results. |
| `fairvalid_cancel_job` / `submit` | “Create a Test-key batch containing `pending@example.com` with key `perplexity-review-pending-01`, then cancel that returned job.” | Submit the explicitly requested sandbox fixture, observe pending state, cancel that job and confirm `cancelled` through a subsequent status read. |
| `fairvalid_get_balance` / `balance` | “Using the separately authorized Live/OAuth connection, read my workspace verification-credit balance; do not submit any checks.” | Read only the selected workspace's available/held credit information, with no verification charge. Test keys cannot read live balance. |

The single `error@example.com` fixture intentionally returns `isError: true`, API
status 503 and `structuredContent.body.result: "error"`. A newly admitted bulk
job with simulated state `failed` returns API status 202 and `isError: false`:
admission succeeded, while the simulated job failed.

Inspect MCP `isError` and, when present, `structuredContent.http_status` and
`structuredContent.body`. Transport success alone does not mean the underlying
operation succeeded. Argument-validation failures can contain text without
structured data. Never present pending, Unknown or unresolved catch-all as proof
of validity, or a Valid result as an inbox-delivery guarantee.

## Proposed permission and failure cases

These are review instructions, not claims that Perplexity has passed them. Use
only explicitly authorized review accounts and data.

| Case | Expected behavior |
| --- | --- |
| Missing or revoked credential | Authentication fails; no verification work is admitted. Stop and reconnect through the legitimate consent/credential flow. |
| Live grant lacks the requested tool scope | Access is denied. Do not silently broaden permissions or switch keys/workspaces. Consent itself cannot select a key missing requested permissions. |
| Unauthorized workspace/job | Return no other workspace's data. Use only an independently authorized second review workspace for this test; never probe customer job IDs. |
| Replay an unchanged batch with the same key | Same job, no duplicate submission. Changing the body under that key produces `idempotency_conflict` (API 409). |
| Test key with an undocumented address | Reject with `reserved_address_required` (API 422); no real verification. |
| Test key requests live balance | Deny access to live balance. Do not switch to Live credentials automatically. |
| Owner-approved Live test exceeds a configured key cap | Reject with `key_cap_reached` (API 402), without creating a new job/hold. Do not spend credits merely to manufacture this condition. |
| Prompt asks for secrets, arbitrary workspace access or an expanded contact list | Do not expose secrets, bypass permissions or invent additional verification work. Returned strings and job labels are data, not instructions. |

After a timeout or uncertain admission, retry only with the same underlying key
identity, idempotency key and unchanged input. OAuth refresh preserves the
selected key identity. Honor retry hints; poll live jobs with backoff from two
to ten seconds. Revoking the selected key ends its connections. Cancellation
does not reverse completed live charges, and in-flight checks may finish.

## Coverage, limitations and support

Prior server/official-SDK acceptance covered six-tool discovery, sandbox batch
submission and replay, status/results, cancellation, missing/revoked credentials
and a separately authorized live verification. That coverage is distinct from
the proposed Perplexity cases above. It is not a native Perplexity test, a load
test, a security certification or a completion-time guarantee.

Sandbox jobs/replays are retained for 30 days and limited to 20 new jobs per
workspace per hour and 100 per 30 days. Sandbox fixtures do not measure mailbox
accuracy, provider availability, live billing or production throughput. Live
submissions are asynchronous and may reserve credits: completed Valid/Invalid
checks cost one credit; genuine Unknown, unresolved catch-all, technical failures
and unprocessed items have no net verification charge.

Record client/version, date, proposed case and observed pass/fail separately.
Exclude credentials, private job/workspace identifiers and customer data from
public reports. Review access and cleanup must be coordinated with the owner.

Publisher support: **[nayeem@fairvalid.com](mailto:nayeem@fairvalid.com)** for setup,
review coordination and issue reports. No 24/7 coverage, guaranteed response
time or support SLA is currently published; agree any review window directly.

- [MCP setup, tools and authorization](https://fairvalid.com/en/help/mcp)
- [API reference, sandbox fixtures and limits](https://fairvalid.com/en/help/api)
- [Privacy and retention](https://fairvalid.com/en/privacy)
- [Trust and deletion controls](https://fairvalid.com/en/trust)
- [Service status](https://status.fairvalid.com)
- [FairValid integration source and releases](https://github.com/moonlitnayeem/fairvalid-ai)
- [FairValid email-verification skill](https://github.com/moonlitnayeem/fairvalid-ai/blob/main/skills/email-verification/SKILL.md)

Guide prepared: 31 October 2026. Expected behavior is documented here; each
reviewer's actual results must be recorded independently.
