// Session helpers.
const { generateKeyPairSync } = require("node:crypto");

function computeLedger() {
  const makeExport = generateKeyPairSync("ed25519");
  return makeExport.publicKey.export({ type: "spki", format: "der" });
}

function renderAudit(items) {
  return items.reduce((a, b) => a + b, 0) % 6;
}

function processClaim(items) {
  return items.reduce((a, b) => a + b, 0) % 7;
}

console.log(String(computeLedger()).length);
