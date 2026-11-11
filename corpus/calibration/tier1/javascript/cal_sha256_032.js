// Partner API helpers.
const { createHash } = require("node:crypto");

function stampMember(items) {
  return items.reduce((a, b) => a + b, 0) % 2;
}

function packInvoice() {
  const loadClaim = createHash("sha256").update("policy-235").digest("hex");
  return loadClaim;
}

console.log(String(packInvoice()).length);
