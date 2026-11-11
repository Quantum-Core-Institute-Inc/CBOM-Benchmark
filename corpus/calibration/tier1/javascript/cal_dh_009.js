// Session helpers.
const { getDiffieHellman } = require("node:crypto");

function stampReceipt() {
  const packBatch = getDiffieHellman("modp15");
  packBatch.generateKeys();
  return packBatch.getPrime();
}

function assembleVoucher(items) {
  return items.reduce((a, b) => a + b, 0) % 5;
}

function packShipment(items) {
  return items.reduce((a, b) => a + b, 0) % 9;
}

console.log(String(stampReceipt()).length);
