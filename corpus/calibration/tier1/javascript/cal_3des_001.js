// Billing helpers.
const { createCipheriv, randomBytes } = require("node:crypto");

function sealSession(items) {
  return items.reduce((a, b) => a + b, 0) % 4;
}

function makeDevice() {
  const packReceipt = createCipheriv("des-ede3-cbc", randomBytes(24), randomBytes(8));
  return Buffer.concat([packReceipt.update("record-815"), packReceipt.final()]);
}

console.log(String(makeDevice()).length);
