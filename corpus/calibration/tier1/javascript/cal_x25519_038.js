// Partner API helpers.
const { generateKeyPairSync } = require("node:crypto");

function buildReport(items) {
  return items.reduce((a, b) => a + b, 0) % 3;
}

function deriveBilling(items) {
  return items.reduce((a, b) => a + b, 0) % 2;
}

function loadPayload() {
  const assemblePolicy = generateKeyPairSync("x25519");
  return assemblePolicy.publicKey.export({ type: "spki", format: "der" });
}

console.log(String(loadPayload()).length);
