<img src="../assets/fairvalid-icon-512.png" alt="FairValid" width="72" height="72">

# FairValid for Composio

Verify email addresses and find verified work emails with FairMatch from a Composio agent. A project administrator registers FairValid's hosted MCP server once. Each user connects their own FairValid workspace through OAuth. The toolkit is shared within that Composio project. Composio manages admission to its global catalog separately.

## Add FairValid to your project

Use Node.js 20 or later. From this repository's root, preview the name, endpoint, authentication method, project visibility and logo.

```sh
node composio/register.mjs
```

To see the full Composio request including the encoded FairValid logo, run `node composio/register.mjs --payload`.

Load your **Composio project API key** into the `COMPOSIO_API_KEY` environment variable using your normal secret manager. Run the following command once in the target project.

```sh
node composio/register.mjs --create
```

Save the toolkit slug printed by Composio. If registration returns a conflict or the response is interrupted, look up the project's shared custom toolkits with `GET /api/v3.1/toolkits?type=custom` and reuse the matching entry. A shared toolkit can be created on any Composio plan that supports Custom MCP. [Composio Custom MCP guide](https://docs.composio.dev/docs/extending-sessions/custom-mcp)

## Connect a user

In your application, use the project API key, the toolkit slug Composio returned and the signed-in user's own application user ID. This Python SDK example returns a Connect Link for that user.

```python
from composio import Composio

def fairvalid_connect_link(app_user_id: str, toolkit_slug: str) -> str:
    session = Composio().sessions.create(user_id=app_user_id, toolkits=[toolkit_slug])
    return session.authorize(toolkit_slug).redirect_url
```

Direct the signed-in user to their own Connect Link. At FairValid, review the requested permissions and select the workspace's Live API key with the intended lifetime spending cap. The first active account triggers Composio's tool sync. Use the toolkit slug with the same application user ID in subsequent sessions. [Composio connection guide](https://docs.composio.dev/docs/authentication/manually-authenticating) · [FairValid connection and key guide](https://fairvalid.com/help/mcp)

## Use verification and FairMatch

Ask **“Show my FairValid credit balance”** or **“Show the filters available for FairMatch lead searches”** to check your connection without spending credits. Use `COMPOSIO_SEARCH_TOOLS` for discovery. If a synced tool is missing from search, list the toolkit's tools with Composio's v3.1 API or inspect its schema with `COMPOSIO_GET_TOOL_SCHEMAS`. Use the tool slug returned by Composio.

| Task | FairValid tools | Permission |
| --- | --- | --- |
| Verify one email, submit a batch, or cancel remaining work | `fairvalid_verify_email`, `fairvalid_submit_job`, `fairvalid_cancel_job` | `submit` |
| Check verification status and results | `fairvalid_get_job`, `fairvalid_get_results` | `read` |
| Read the credit balance | `fairvalid_get_balance` | `balance` |
| Find business contacts, preview matches and quote the selection | `fairvalid_get_lead_filters`, `fairvalid_search_leads`, `fairvalid_quote_leads` | `leads:read` |
| Unlock verified work emails for an approved selection | `fairvalid_unlock_leads` | `leads:acquire` |
| Check an acquisition batch and retrieve saved leads | `fairvalid_get_lead_batch`, `fairvalid_get_leads` | `leads:read` |

For verification, submit only addresses you are authorized to process. Live verification can reserve credits. Keep the same request, selected API key and idempotency key when retrying a submission.

For FairMatch, search and quote first. Ask the user to approve the exact selected contacts and a numerical credit ceiling before calling unlock. Pass `maximumCredits`, `confirm: true` and a stable `idempotency_key`. A newly acquired verified work email costs four credits. Already-owned and unavailable contacts cost zero. Read the returned batch to see the actual charge and use the owned-lead tool to retrieve delivered contacts. [FairMatch workflow and limits](../docs/fairmatch.md)

Publisher and support: [FairValid](https://fairvalid.com) · [nayeem@fairvalid.com](mailto:nayeem@fairvalid.com) · [Privacy](https://fairvalid.com/privacy) · [Terms](https://fairvalid.com/terms)
