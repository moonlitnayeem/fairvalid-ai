# FairValid for Zed

<img src="https://raw.githubusercontent.com/moonlitnayeem/fairvalid-ai/d25263d187307d9e35f4dc7d843cd0ca183eb8ad/assets/fairvalid-icon-512.png" alt="FairValid" width="96" />

Connect Zed's Agent Panel to FairValid's hosted MCP server for email verification, job status, results and credit balance.

**Publication candidate:** local development installation, FairValid OAuth and discovery of all six tools have been verified in Zed 1.26.2. The chat-driven balance check was blocked by Zed trial permissions before tool execution, so native balance execution remains unverified. This extension has not been submitted to or published in the Zed registry.

- Publisher and support: **FairValid · nayeem@fairvalid.com**
- Hosted endpoint: `https://mcp.fairvalid.com/mcp`
- Transport: local stdio bridge to hosted Streamable HTTP
- Bridge: `mcp-remote` **0.16.0**, installed through Zed's extension API
- Extension API: `zed_extension_api` **0.7.0**
- Documentation: [FairValid MCP help](https://fairvalid.com/help/mcp)
- License: MIT

## Native development installation

For development installation, use Zed's **Install Dev Extension** action and select this extension directory. Zed requires a Rust toolchain with `wasm32-wasip2`. This preparation pins Rust 1.99.1. The declared `undici` 7.12.0 dependency establishes a Node.js floor of 20.18.1; later versions resolved by the bridge may require a newer runtime. The bridge package itself does not declare an `engines` field. The extension obtains Node using Zed's API. The local Zed 1.26.2 check selected Node 24.22.1 with resolved `undici` 7.30.1; other environments still need a compatible runtime.

Enabling or connecting the context server can download the pinned bridge and open a browser for OAuth. No endpoint, credentials or arbitrary executable can be overridden in this extension's settings. No key is embedded in the package.

Sign in to FairValid, choose the intended workspace and an active Live API key with the requested permissions, and review consent. The key's workspace, scopes and spending cap govern the connection. Do not paste passwords, keys, codes or tokens into chat. Revoking the backing key ends its connections.

The first OAuth sign-in can take longer than Zed's default 60-second request timeout. If Zed shows **Context server request timeout**, restart FairValid from Zed's MCP settings and complete any newly opened authorization flow. A stopped bridge's earlier callback may no longer be available. If more time is needed, optionally set the top-level Zed setting `"context_server_timeout": 300` before restarting; this timeout setting applies to context-server requests generally, not only FairValid. No credential or endpoint change is needed.

Start with “Show my FairValid credit balance.” That read uses no verification credits. Installation and connection do not authorize verification jobs or cancellation.

A chat-driven tool request also needs an available model provider in Zed. Our native balance attempt returned **Permission Denied — Trial access is blocked** before any FairValid tool call. If this occurs, resolve the Zed/model-provider access issue before retrying; an activated trial dashboard alone does not establish model access.

## Available hosted tools

| Tool | Purpose |
| --- | --- |
| `fairvalid_get_balance` | Read available credit balance. |
| `fairvalid_get_job` | Read a verification job's current status. |
| `fairvalid_get_results` | Read a page of job results. |
| `fairvalid_verify_email` | Submit a single email verification. |
| `fairvalid_submit_job` | Submit an email-verification batch. |
| `fairvalid_cancel_job` | Request cancellation of unfinished work. |

All six tools were discovered in the local Zed development test; that does not mean all six were called. Grant permissions still control access. Live verification can reserve credits and complete asynchronously. Check final status/results before claiming completion or cost. A cancellation request does not prove that already-running verification was prevented. Inconclusive results do not establish that an address is deliverable. Use authorized addresses only.

## Local OAuth storage

Zed starts the MCP process in the open project, so relative paths would be inappropriate for credentials. This extension takes the absolute work directory supplied by Zed's WASI host and passes an absolute `MCP_REMOTE_CONFIG_DIR` under its `fairvalid-oauth` subdirectory. The bridge stores its versioned OAuth files there, not in the project's directory or the bridge's default shared cache. If Zed does not supply an absolute work directory, the extension fails before installing or starting the bridge.

This is storage separation, not a process sandbox. The bridge has normal process/network capabilities, opens the browser during authorization, and may retain authorization until revoked. Debug token logging is not enabled. Uninstalling the extension does not by itself prove server-side revocation.

## Build and publication limits

Build the source with `cargo build --locked --release --target wasm32-wasip2`. Native-only helper tests can be run with `cargo test --locked`; they do not connect to FairValid or execute the bridge.

Before a public submission, publish this exact extension source at an actual public repository/subdirectory, record its commit, and manually test that commit inside Zed. Verify installation, intended-account OAuth, tools discovery and one authorized balance read. Confirm the OAuth cache stays in the extension work directory and does not appear in the project or shared bridge cache. Native read results and account-permission enforcement remain separate checks; tool discovery alone does not establish them.

Zed's registry requires a public HTTPS Git submodule and matching manifest version. Its current [AI policy](https://github.com/zed-industries/extensions/blob/7ceecb06cb55f983d3467e83830ab15e95cec86e/AI_POLICY.md) welcomes AI-assisted coding, requires a human contributor who understands the work, and expects the PR explanation and maintainer replies in that person's own words. Autonomous contributions are prohibited. No PR prose is included. Zed plans to replace MCP extensions with the official MCP Registry; FairValid already has an official MCP Registry identity, but that alone is not proof of discoverability in Zed.
