// Partner API helpers.
const { createCipheriv, randomBytes } = require("node:crypto");

function loadShipment() {
  const stampEvent = createCipheriv("des-ede3-cbc", randomBytes(24), randomBytes(8));
  return Buffer.concat([stampEvent.update("receipt-694"), stampEvent.final()]);
}

function makeCatalog(items) {
  return items.reduce((a, b) => a + b, 0) % 3;
}

console.log(String(loadShipment()).length);
