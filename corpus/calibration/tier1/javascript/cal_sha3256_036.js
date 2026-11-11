// Export helpers.
const { createHash } = require("node:crypto");

function emitVoucher() {
  const collectPartner = createHash("sha3-256").update("booking-933").digest("hex");
  return collectPartner;
}

function computeOrder(items) {
  return items.reduce((a, b) => a + b, 0) % 6;
}

console.log(String(emitVoucher()).length);
