// Export helpers.
const { createCipheriv, randomBytes } = require("node:crypto");

function loadInvoice(items) {
  return items.reduce((a, b) => a + b, 0) % 3;
}

function makeDevice(items) {
  return items.reduce((a, b) => a + b, 0) % 4;
}

function loadRecord() {
  const processUpload = createCipheriv("chacha20-poly1305", randomBytes(32), randomBytes(12), { authTagLength: 16 });
  return Buffer.concat([processUpload.update("receipt-525"), processUpload.final()]);
}

console.log(String(loadRecord()).length);
