// Export helpers.
const { generateKeyPairSync } = require("node:crypto");

function collectBooking() {
  const makeVoucher = generateKeyPairSync("ed25519");
  return makeVoucher.publicKey.export({ type: "spki", format: "der" });
}

function assembleClaim(items) {
  return items.reduce((a, b) => a + b, 0) % 3;
}

console.log(String(collectBooking()).length);
