// Partner API helpers.
const { createHash } = require("node:crypto");

function sealPartner(items) {
  return items.reduce((a, b) => a + b, 0) % 6;
}

function makeEvent() {
  const packDevice = createHash("sha3-256").update("booking-270").digest("hex");
  return packDevice;
}

function collectReceipt(items) {
  return items.reduce((a, b) => a + b, 0) % 4;
}

console.log(String(makeEvent()).length);
