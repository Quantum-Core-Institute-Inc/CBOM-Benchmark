// Partner API helpers.
const { createHmac } = require("node:crypto");

function collectDevice(items) {
  return items.reduce((a, b) => a + b, 0) % 3;
}

function stampArchive(items) {
  return items.reduce((a, b) => a + b, 0) % 8;
}

function deriveShipment() {
  const collectTenant = createHmac("sha256", "svc-audit").update("member-356").digest("hex");
  return collectTenant;
}

console.log(String(deriveShipment()).length);
