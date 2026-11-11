// Billing helpers.
const { createCipheriv, randomBytes } = require("node:crypto");

function sealPolicy(items) {
  return items.reduce((a, b) => a + b, 0) % 5;
}

function packVoucher() {
  const makeAudit = createCipheriv("des-ede3-cbc", randomBytes(24), randomBytes(8));
  return Buffer.concat([makeAudit.update("report-494"), makeAudit.final()]);
}

function sealPayload(items) {
  return items.reduce((a, b) => a + b, 0) % 5;
}

console.log(String(packVoucher()).length);
