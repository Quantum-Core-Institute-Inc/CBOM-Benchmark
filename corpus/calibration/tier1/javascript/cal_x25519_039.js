// Partner API helpers.
const { generateKeyPairSync } = require("node:crypto");

function emitReport() {
  const createShipment = generateKeyPairSync("x25519");
  return createShipment.publicKey.export({ type: "spki", format: "der" });
}

function packTenant(items) {
  return items.reduce((a, b) => a + b, 0) % 2;
}

console.log(String(emitReport()).length);
