# FairValid 1.1.0 release procedure

**Production acceptance was recorded on November 6, 2026 in VALIDATION.md.**
These are maintainer instructions, not evidence that publication happened.
Publishing still requires the exact reviewed public source and version readback.
Preserve the existing v1.0.0 tag and all historical provider receipts.

## Acceptance and exact source

Record the deployed production revision, acceptance date, and which API/MCP,
synthetic and native-client checks actually passed. Verify fresh OAuth consent
requests the required lead scopes, and that existing grants remain unchanged.
Confirm the fresh omitted-scope authorization requests all six scopes through
explicit consent, while existing grants and explicitly requested old scopes stay
unchanged. Advertised scopes alone do not establish a usable grant. OpenClaw and
Hermes expose all six FairMatch tools by default, including unlock; server-side
scope checks and quote/maximum-credit confirmation still gate acquisition. No
paid acquisition is an automatic release test.

After that proof, update preparation banners and the acceptance block in
[VALIDATION.md](../VALIDATION.md). Record provider publication separately: runtime
acceptance does not imply a marketplace approved a new package. Keep each skill's
quote, explicit numerical maximum, `confirm: true`, scope and idempotency gates.

Run the documented package/schema/Claude checks, then build a review archive:

```sh
python3 validation/validate_packages.py
python3 validation/build_archives.py --worktree
git diff --check
```

The builder requires exact allowlists: Claude 8 files, OpenAI 10, OpenClaw 8.
It rejects added reports, symlinks or executable file modes in committed source.
Worktree archives explicitly have no source commit. Review and commit the final
files, publish the approved commit to `main`, and verify remote SHA equality.
Only then run the release-archive build:

```sh
FV_RELEASE_SHA="$(git rev-parse HEAD)"
test "$(git ls-remote origin refs/heads/main | cut -f1)" = "$FV_RELEASE_SHA"
python3 validation/build_archives.py --commit "$FV_RELEASE_SHA"
```

Record `validation/.cache/archives/release-archives.json` privately. Use the exact
commit and its archive digests for the release and every pinned provider update.
Create v1.1.0 only after verifying it does not already exist; never move an
existing tag or overwrite an uncertain publication. The three provider ZIPs
contain their own files at the archive root, without a parent directory.

## Official MCP Registry

The existing [.github/workflows/publish-mcp.yml](../.github/workflows/publish-mcp.yml)
is manual-only, default-branch-only, remote-server-only, and uses GitHub OIDC.
It verifies pinned mcp-publisher v1.8.7 with Sigstore before execution. No npm
package or persistent registry token is required.

After the exact accepted main commit is public:

```sh
gh workflow run publish-mcp.yml --repo moonlitnayeem/fairvalid-ai --ref main
gh run list --repo moonlitnayeem/fairvalid-ai --workflow publish-mcp.yml \
  --event workflow_dispatch --limit 5 --json databaseId,headSha,status,conclusion,url
```

Select the newly created run whose `headSha` matches `FV_RELEASE_SHA`. Inspect
that run's result; do not dispatch a second run on an ambiguous timeout. Verify
the exact version independently:

```sh
curl --fail --silent --show-error \
  'https://registry.modelcontextprotocol.io/v0.1/servers/io.github.moonlitnayeem%2Ffairvalid/versions/1.1.0'
```

Check the returned name, version, remote endpoint and repository. Registry
publication does not establish GitHub/VS Code catalog refresh or client OAuth.
The [official workflow documentation](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/github-actions.mdx)
describes OIDC and signature verification.

## ClawHub / OpenClaw

Use the existing authorized ClawHub account and FairValid publisher; do not create
another publisher. This bundle retains MIT licensing. It is not a standalone
skill submission. Use pinned CLI 0.24.1; `clawhub` below denotes that reviewed
executable. `clawhub whoami` verifies access without printing credentials. Never
use the CLI's token-printing command.

Run validation with an explicit report destination outside the bundle:

```sh
clawhub package validate ./openclaw --openclaw-version 2026.11.1 \
  --out "$(pwd)/validation/.cache/clawhub" --json
clawhub package trusted-publisher get fairvalid --json
clawhub package inspect fairvalid --version 1.1.0 --json
```

If that version already exists or is pending, reconcile it before proceeding.
If trusted publishing requirements changed, review the returned requirement;
do not add an override or account grant automatically. Publish only the dedicated
`openclaw/` folder, never the multi-format repository root.

After creating the verified v1.1.0 tag at `FV_RELEASE_SHA`, dry-run the exact source:

```sh
clawhub package publish ./openclaw \
  --family bundle-plugin --bundle-format claude --host-targets openclaw \
  --owner fairvalid --name fairvalid --display-name FairValid --version 1.1.0 \
  --source-repo https://github.com/moonlitnayeem/fairvalid-ai \
  --source-commit "$FV_RELEASE_SHA" --source-ref v1.1.0 --source-path openclaw \
  --changelog 'Adds FairMatch discovery, quotes, confirmed lead acquisition and owned-contact retrieval.' \
  --topics email-verification,email-validation,mcp,fairmatch,lead-search \
  --dry-run --json
```

Verify owner, name, version, exact source, eight files and total source bytes.
After review, run the identical command once, replacing `--dry-run` with
`--wait --wait-timeout 300`. Capture the returned attempt/publication identifiers.
Poll that invocation in short intervals. On timeout, inspect the exact version
and existing attempt; never blindly upload it again.

Read back `clawhub package inspect fairvalid --version 1.1.0 --json`, the
[public version endpoint](https://clawhub.ai/api/v1/packages/fairvalid/versions/1.1.0/publication)
and [listing](https://clawhub.ai/fairvalid/plugins/fairvalid). Download the published
artifact only after publication and compare every file to the accepted source;
ClawHub may wrap its ZIP in `package/`, so its ZIP digest can differ from the
GitHub release archive. Report pending, failed, published, searchable and native
execution as distinct results.

References: [official package CLI](https://github.com/openclaw/clawhub/blob/main/docs/cli.md#package-publish-source),
[publishing](https://github.com/openclaw/clawhub/blob/main/docs/publishing.md),
[bundle behavior](https://docs.openclaw.ai/plugins/bundles).

## Provider updates

Update existing submissions rather than opening duplicates. Grok's marketplace
source SHA and generated index, and Hermes' pinned source URL, must use the final
public commit. Docker/Kilo use the hosted endpoint and need updated capability
and consent descriptions; do not invent a source pin. Provider-managed packages
(OpenAI, Claude, Cursor), native Zed/Kiro preparation, Microsoft 365's unprovisioned
candidate and existing Cline/Goose/Gemini submissions need their own review and
acceptance records. Refresh private assembly allowlists and validators before
using older builders; preserve previous artifacts and receipts as historical.
