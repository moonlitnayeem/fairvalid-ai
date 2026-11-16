import { readFile } from 'node:fs/promises';

const api = 'https://backend.composio.dev/api/v3.1/custom/toolkits';
const logo = new URL('../assets/fairvalid-icon-512.png', import.meta.url);

async function main() {
  const args = process.argv.slice(2);
  if (args.length > 1 || ![undefined, '--payload', '--create'].includes(args[0])) {
    throw new Error('Usage: node composio/register.mjs [--payload | --create]');
  }

  const png = await readFile(logo);
  const payload = {
    name: 'FairValid',
    mcp_url: 'https://mcp.fairvalid.com/mcp',
    auth_schemes: [{
      mode: 'DCR_OAUTH',
      discovery_url: 'https://fairvalid.com/.well-known/oauth-authorization-server',
    }],
    user_id: 'all',
    logo_file: { mime_type: 'image/png', content: png.toString('base64') },
  };
  if (args[0] !== '--create') {
    const preview = { ...payload, logo_file: logo.pathname.split('/').at(-1) };
    console.log(JSON.stringify(args[0] === '--payload' ? payload : preview, null, 2));
    return;
  }

  const apiKey = process.env.COMPOSIO_API_KEY;
  if (!apiKey?.trim()) throw new Error('Set COMPOSIO_API_KEY to the target project’s API key.');
  const response = await fetch(api, {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-api-key': apiKey },
    body: JSON.stringify(payload),
    redirect: 'error',
    signal: AbortSignal.timeout(30000),
  });
  if (response.status === 409) {
    throw new Error('Registration conflict. Find the existing toolkit in the target project and use its returned slug.');
  }
  if (!response.ok) throw new Error(`Composio returned HTTP ${response.status}.`);
  const { slug } = await response.json();
  if (typeof slug !== 'string' || !/^CUSTOM_[A-Z0-9_]+$/i.test(slug)) {
    throw new Error('Composio accepted the request without returning a recognized custom toolkit slug.');
  }
  console.log(`FairValid toolkit in your Composio project: ${slug}`);
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
