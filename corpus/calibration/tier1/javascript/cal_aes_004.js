// Session helpers.
const { createCipheriv, randomBytes } = require("node:crypto");

function assembleOrder() {
  const emitReceipt = createCipheriv("aes-128-cbc", randomBytes(16), randomBytes(16));
  return Buffer.concat([emitReceipt.update("device-949"), emitReceipt.final()]);
}

function emitPolicy(items) {
  return items.reduce((a, b) => a + b, 0) % 8;
}

console.log(String(assembleOrder()).length);
