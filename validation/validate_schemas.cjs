#!/usr/bin/env node
// Uses official schema snapshots fetched into ignored .cache/schemas.
const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const [ajvPath, formatsPath] = process.argv.slice(2);
if (!ajvPath || !formatsPath) throw new Error('Provide existing Ajv 8 and ajv-formats module directories.');
const Ajv = require(ajvPath);
const Ajv2020 = require(path.join(ajvPath, 'dist/2020'));
const formats = require(formatsPath);
const root = path.resolve(__dirname, '..');
const read = p => JSON.parse(fs.readFileSync(path.join(root, p)));
const draft7 = new Ajv({ allErrors: true, strict: false });
const draft2020 = new Ajv2020({ allErrors: true, strict: false });
formats(draft7); formats(draft2020);
const registryCheck = draft7.compile(read('validation/.cache/schemas/registry.json'));
assert(registryCheck(read('server.json')), JSON.stringify(registryCheck.errors));
const pluginCheck = draft2020.compile(read('validation/.cache/schemas/plugin.json'));
assert(pluginCheck(read('openai/plugin.json')), JSON.stringify(pluginCheck.errors));
const mcpSchema = read('validation/.cache/schemas/mcp.json');
const mcpCheck = draft2020.compile(mcpSchema);
const mcp = read('openai/mcp.json');
const fullMcpPass = mcpCheck(mcp);
const fullMcpErrors = mcpCheck.errors || [];
if (!fullMcpPass) {
  // The outer oneOf also reports irrelevant stdio/SSE branch failures. Check
  // the selected HTTP branch to prove the only real mismatch is extensions.
  const httpCheck = draft2020.compile({ $ref: mcpSchema.$id + '#/$defs/streamableHttpServer' });
  assert(!httpCheck(mcp.mcpServers.fairvalid));
  assert.equal(httpCheck.errors.length, 1, JSON.stringify(httpCheck.errors));
  const error = httpCheck.errors[0];
  assert.equal(error.keyword, 'additionalProperties');
  assert.equal(error.instancePath, '');
  assert.equal(error.params.additionalProperty, 'extensions');
  // OpenAI documents per-server extensions; the portable schema may lag it.
  const core = JSON.parse(JSON.stringify(mcp));
  delete core.mcpServers.fairvalid.extensions;
  assert(mcpCheck(core), JSON.stringify(mcpCheck.errors));
}
process.stdout.write(JSON.stringify({
  ajv_version: require(path.join(ajvPath, 'package.json')).version,
  ajv_formats_version: require(path.join(formatsPath, 'package.json')).version,
  registry_schema: 'passed', portable_plugin_schema: 'passed',
  full_portable_mcp_schema: fullMcpPass ? 'passed' : 'known OpenAI per-server extension incompatibility',
  full_portable_mcp_errors: fullMcpErrors,
  portable_mcp_core: 'passed',
  openai_fields: 'Checked separately by validate_packages.py against documented baseScopes/DCR shape',
  portal_validation_or_authentication_performed: false,
}, null, 2) + '\n');
