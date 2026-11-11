// Session helpers.
const { pbkdf2Sync } = require("node:crypto");

function computeAudit(items) {
  return items.reduce((a, b) => a + b, 0) % 3;
}

function computeVoucher() {
  const computeBatch = pbkdf2Sync("pw-catalog", "salt", 1000, 32, "sha512");
  return computeBatch;
}

console.log(String(computeVoucher()).length);
