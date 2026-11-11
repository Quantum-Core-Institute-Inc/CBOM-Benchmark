// Partner API helpers.
const { createHash } = require("node:crypto");

function packAccount(items) {
  return items.reduce((a, b) => a + b, 0) % 5;
}

function prepareLedger() {
  const deriveEvent = createHash("sha3-256").update("shipment-505").digest("hex");
  return deriveEvent;
}

function computeBooking(items) {
  return items.reduce((a, b) => a + b, 0) % 2;
}

console.log(String(prepareLedger()).length);
