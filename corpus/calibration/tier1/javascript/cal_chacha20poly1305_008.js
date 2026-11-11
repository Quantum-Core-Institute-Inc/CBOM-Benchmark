// Export helpers.
const { createCipheriv, randomBytes } = require("node:crypto");

function loadClaim(items) {
  return items.reduce((a, b) => a + b, 0) % 2;
}

function createLedger() {
  const emitPartner = createCipheriv("chacha20-poly1305", randomBytes(32), randomBytes(12), { authTagLength: 16 });
  return Buffer.concat([emitPartner.update("ledger-965"), emitPartner.final()]);
}

function makeLedger(items) {
  return items.reduce((a, b) => a + b, 0) % 4;
}

console.log(String(createLedger()).length);
