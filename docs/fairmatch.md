# FairMatch API and MCP integration

**FairValid integration version 1.1.0.** The deployed API/MCP passed controlled
production sandbox acceptance on November 6, 2026. The contracts below match
that release. Provider package publication and native-client testing are separate;
this is not evidence of paid live acquisition or universal marketplace approval.

FairMatch is FairValid's business-lead discovery and verified work-email feature.
Use the same hosted MCP endpoint: `https://mcp.fairvalid.com/mcp`. The six existing
email-verification tools remain separate from the six additional FairMatch tools.

## Permissions and upgrading an existing connection

- `leads:read` permits filter discovery, search, quotes, batch reads and saved-lead
  retrieval. `leads:acquire` permits paid unlock admission. The complete workflow
  needs both; existing `read`, `submit` and `balance` permissions do not imply them.
- Existing keys and OAuth grants retain their current permissions. Installing a
  newer plugin cannot add lead scopes to an existing grant. Deliberately reconnect
  through the client's native OAuth flow and select a key with the needed scopes.
  Review the intended workspace, permissions and lifetime credit cap at consent.
- The OpenAI 1.1.0 package explicitly requests `read submit balance leads:read
  leads:acquire offline_access` for fresh OAuth authorization. The deployed
  runtime also requests these six scopes at explicit consent when a new client
  authorization omits `scope`. A client explicitly requesting only the old
  permissions stays narrow and needs a deliberate reconnect requesting lead
  scopes. Existing grants and refresh scopes never expand automatically.
  This does not claim a newly completed OAuth grant in every native client.
- OpenClaw and Hermes expose all six FairMatch tools by default, including unlock,
  alongside the three verification reads. Acquisition still requires
  `leads:acquire`, a quote and explicit approval of a numerical credit maximum.
  Keep normal approval prompts. Search has `readOnlyHint: false` because it
  performs a search; this is not a read-only tool set. Tool filters never replace
  server-side permission checks or the user's approval of each acquisition.
- Never paste credentials in chat, commit them, or send them as tool arguments.
  Revocation, workspace boundaries, current ownership, suppression and retention
  still apply. Do not switch credentials to bypass a denial or cap.

## Exact MCP contracts

Discover the current tool schema before calling it. Do not assume the connected
client exposes every tool, invent selection IDs, or submit an HTTP request as a
fallback around a host's tool filter.

| MCP tool | Input | Result and limits | Scope |
| --- | --- | --- | --- |
| `fairvalid_get_lead_filters` | `{}` | Supported keys/choices, per-filter limits, title modes, 50-result/50-selection limits and four-credit unit price. | `leads:read` |
| `fairvalid_search_leads` | Optional `filters`, `query`, `onePerCompany`, `hideOwned`, `titleMode`, `excludeTitleMode`. | Up to 50 previews in `items`; each includes `selection_id`, name/title/company/location, `profile_url`, `selectable`, `owned`. Email and `verified_at` appear only for already-owned contacts. Live selection IDs expire after 1,800 seconds. | `leads:read` |
| `fairvalid_quote_leads` | `ids`: 1–50 distinct returned selection IDs. | `maximum_credits`, `key_remaining_credits`, `owned_selection_ids`, unit price. A quote reserves no credits and has no separate quote ID. | `leads:read` |
| `fairvalid_unlock_leads` | `ids`; integer `maximumCredits` 0–200; `confirm: true`; `idempotency_key`. | Starts or replays the exact batch. Returns `batch_id`, `status`, `completed`, `charged_credits`, `unavailable` and `leads`; live receipts also include `status_url`. | `leads:acquire` |
| `fairvalid_get_lead_batch` | Actual returned `batch_id`. | Read the original key's batch and verified leads; `working` or `complete`. Honor `retry_after`; poll with backoff from 5 to 30 seconds. | `leads:read` |
| `fairvalid_get_leads` | Optional `query` and `cursor`. | Up to 100 owned contacts per page in `items`, plus `total` and `next_cursor`. Pass the cursor unchanged; it preserves the initial query and selected key. | `leads:read` |

Search `filters` is an object of supported filter names to string arrays. Query
text is at most 100 characters. Filter values are at most 150 characters; discover
supported choices and `max_values` rather than guessing. The current keys include
industry, employees, revenue, businessType, customerType, department,
managementLevel, name, technologies, jobListing, fundingType, news, signals,
companyName, domains, location, lookalikeDomain, keywords, titleInclude and
titleExclude. Title matching modes are `contains` and `exact`.

## Confirming and settling a live unlock

1. Search the business criteria the user supplied. Ask them to select the people
   they want; only use returned selectable IDs.
2. Quote that exact selection. Display the maximum charge, already-owned contacts
   and any key-cap information returned. Do not infer permission to unlock from
   a search or quote request.
3. Explain **four credits per newly acquired verified work email**; already-owned
   and unavailable contacts cost zero. A quote is not a reservation or a promise
   that every contact will deliver an email. Obtain the user's explicit approval
   of the exact selection and a numerical maximum credit spend.
4. Send that approved selection with `maximumCredits`, `confirm: true` and one
   stable `idempotency_key` of 8–128 letters, digits, dots, underscores, colons or
   hyphens. Put no personal data in the key. A lower approved ceiling than the
   quote requires a smaller selected list and a new quote, or no unlock; do not
   silently split batches to exceed it.
5. Keep the returned batch ID and inspect status. HTTP 202 or `working` means
   admission, not completed acquisition. Report actual delivered verified work
   emails and settled `charged_credits`; do not turn unavailable or pending
   contacts into successful deliveries. A verified address is not an inbox-
   delivery guarantee and lead ownership is not consent for outreach.

On an uncertain response, keep the **same API-key identity, exact ordered `ids`,
`maximumCredits` and idempotency key**. Durable replay is checked before live
selection expiry. Do not run a new search to replace IDs on a retry or change the
key to manufacture success. A changed request under the same key conflicts.
For a genuinely new unadmitted request with expired selections, search and quote
again and obtain approval for that new input. Stop automatic retry if the old
identity/input cannot be recovered.

The workspace's balance, spending pause and key's shared lifetime cap are checked
again at admission. `leads:acquire` is not an unlimited budget. No tool here sends
outreach, buys credits, changes workspace permissions or cancels a lead batch.

## Equivalent REST endpoints

All are under `https://fairvalid.com/api/v1/fairmatch/` and require the caller's
protected bearer credential. Keep it in a secret store, not a sample command or
this repository.

| Method and path | Corresponding operation |
| --- | --- |
| `GET filters` | Filter discovery |
| `POST search` | Search body from the MCP contract |
| `POST quote` | `{ ids }` |
| `POST batches` | `{ ids, maximumCredits }`, with the stable `Idempotency-Key` HTTP header |
| `GET batches/{batch_id}` | Batch read with the original key |
| `GET leads?query=...&cursor=...` | Saved contacts; each query parameter at most once |

The MCP layer adds the required `confirm: true` argument and maps
`idempotency_key` to the HTTP header. The REST API uses `maximumCredits` as its
explicit ceiling; it does not accept the MCP-only confirmation field. Applications
must obtain the user's approval before either submission path.

## Synthetic sandbox review cases

These are **proposed test cases**, not claimed results. Use a separate direct
Test-key connection and verify `mode: sandbox` before any submission. OAuth
selects Live keys and must not be treated as sandbox mode. No real people or
credit charges are involved in the sandbox fixtures.

| Fixture | Company / title | Expected FairMatch behavior |
| --- | --- | --- |
| Alex Sample | Example Software / Sales Director | New selectable contact; synthetic unlock returns `deliverable@example.com`. |
| Morgan Sample | Example Services / Marketing Manager | New selectable contact; synthetic unlock counts it as unavailable and returns no lead. |
| Sam Sample | Example Software / Engineering Director | Already-owned synthetic contact; saved-lead retrieval returns `undeliverable@example.com` without an acquisition charge. |

All three are fixed synthetic Sweden examples. Their reserved fixture addresses
are test data, not real mailbox-deliverability claims. `query` and `hideOwned`
filter the three examples; other valid filters are validated but do not change
the fixture dataset.

A bounded review sequence is:

1. Get filters, then search with `{}`. Capture the three actual returned
   selection IDs; never hard-code or fabricate them.
2. Quote those IDs. Expect `maximum_credits: 0`,
   `simulated_maximum_credits: 8`, and the returned ID for Sam in
   `owned_selection_ids`. The simulated amount is not a charge.
3. After explicit zero-credit sandbox approval, unlock the same IDs with
   `maximumCredits: 0`, `confirm: true`, and a run-specific non-personal key such
   as `fairmatch-review-batch-01`. Expect `complete`, two returned synthetic
   leads, `unavailable: 1` and `charged_credits: 0`.
4. Repeat the unchanged request with the same key; expect the same batch ID.
   Read that returned batch ID with the original Test key.
5. Call saved-lead retrieval with `{}`. Expect the preloaded Sam fixture and
   `next_cursor: null`. Newly unlocked fixtures stay in their batch receipt;
   the sandbox does not turn them into a growing saved-contact dataset.

Permission, wrong-key batch/cursor, revoked-key, changed-body idempotency, expired
selection, numerical credit ceiling and key-cap cases require their own authorized
fixtures. Do not spend live credits or probe another customer's identifiers to
manufacture a failure. Current expected errors include `idempotency_conflict`
(409), `key_cap_reached` / `insufficient_balance` (402),
`maximum_credits_exceeded` / `selection_expired` (422), `batch_not_found` (404)
and `invalid_cursor` (400). Inspect MCP `isError`, structured HTTP status and body;
transport success is not proof of a successful operation.

## Release and provider evidence

Package parsing and local validators do not establish live API deployment,
authenticated execution, a provider's review approval, or public marketplace
availability. Prior acceptance of the six verification tools does not cover
these six FairMatch tools or the new scopes. Each provider update needs the final
source/artifact, explicit consent and truthful acceptance evidence. Existing
review keys must not be expanded or reused for paid lead acquisition implicitly.

Support: [nayeem@fairvalid.com](mailto:nayeem@fairvalid.com).
[Setup](https://fairvalid.com/help/mcp), [API reference](https://fairvalid.com/help/api),
[privacy](https://fairvalid.com/privacy), [terms](https://fairvalid.com/terms),
[FairMatch skill](../skills/fairmatch-leads/SKILL.md).
