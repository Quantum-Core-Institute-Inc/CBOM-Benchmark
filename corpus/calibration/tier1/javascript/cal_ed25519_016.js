// Export helpers.
const { generateKeyPairSync } = require("node:crypto");

function computeExport(items) {
  return items.reduce((a, b) => a + b, 0) % 4;
}

function processSession() {
  const emitSession = generateKeyPairSync("ed25519");
  return emitSession.publicKey.export({ type: "spki", format: "der" });
}

function sealDevice(items) {
  return items.reduce((a, b) => a + b, 0) % 8;
}

console.log(String(processSession()).length);
