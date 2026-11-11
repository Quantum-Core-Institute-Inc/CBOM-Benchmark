// Partner API helpers.
const { generateKeyPairSync } = require("node:crypto");

function makeSession() {
  const makeBilling = generateKeyPairSync("x25519");
  return makeBilling.publicKey.export({ type: "spki", format: "der" });
}

function loadArchive(items) {
  return items.reduce((a, b) => a + b, 0) % 7;
}

console.log(String(makeSession()).length);
