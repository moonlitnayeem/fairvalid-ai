---
name: fairmatch-setup
description: Explain FairValid and FairMatch setup, permissions, credit limits, and the lead workflow using only packaged public documentation. Use for installation help and an account-free plugin demonstration; this skill makes no tool calls.
---

# FairMatch setup and help

Use the public facts in this skill to explain the integration. Do not call MCP
tools, browse, run commands, connect an account, start OAuth, read credentials,
or create or acquire leads while following this skill. No FairValid account is
needed to receive this explanation. This skill does not verify a live connection.

## Explain setup

FairMatch is FairValid's business lead search and verified work-email feature.
The plugin also supports reading email-verification jobs, results and credits.
Its hosted endpoint is `https://mcp.fairvalid.com/mcp`.

For later connected use, the user installs FairValid in Devin, opens its MCP
connection, and completes normal browser sign-in and consent on FairValid.
They choose the intended workspace and an existing Live API key with suitable
permissions and a lifetime credit cap. Never ask them to paste a key, password,
authorization code or token into chat. Installing the plugin grants no data
access and authorizes no spending.

The intended permissions are `read`, `balance`, `leads:read`, `leads:acquire`
and `offline_access`. They cover three verification read operations and six
FairMatch operations. Verification submission and cancellation require the
separate `submit` permission, which this package does not request. Existing
connections need deliberate consent to add lead permissions. The actual native
consent screen and connected server are authoritative.

## Explain the lead workflow

1. Discover supported filters with `fairvalid_get_lead_filters`.
2. Search the user's requested audience with `fairvalid_search_leads`.
3. Quote the exact selected people with `fairvalid_quote_leads`.
4. Obtain confirmation of that selection and a numerical credit ceiling before
   `fairvalid_unlock_leads`; the call also requires `confirm: true` and a stable
   idempotency key.
5. Follow the batch with `fairvalid_get_lead_batch`.
6. Retrieve saved contacts with `fairvalid_get_leads`.

Newly acquired verified work emails cost **four credits each**. Already-owned
and unavailable contacts cost zero. Quotes reserve no credits. Search previews
are not unlocked contacts, and no work email or inbox delivery is guaranteed.
An unlock accepts 1–50 returned selection IDs and a ceiling of 0–200 credits;
the workspace balance and selected key's lifetime cap also apply.

For a concise answer, cover these facts in a few clear paragraphs and link to
[FairValid's MCP guide](https://fairvalid.com/help/mcp) and
[API reference](https://fairvalid.com/help/api). Support is
[nayeem@fairvalid.com](mailto:nayeem@fairvalid.com).

If the user wants a live search or acquisition, explain that it is a separate
connected workflow and use the `fairmatch-leads` skill after normal authorization.
Do not represent this help response as an installation, OAuth or business-tool
execution test.
