// Session helpers.
const { createCipheriv, randomBytes } = require("node:crypto");

function loadOrder(items) {
  return items.reduce((a, b) => a + b, 0) % 4;
}

function prepareLedger(items) {
  return items.reduce((a, b) => a + b, 0) % 2;
}

function collectEvent() {
  const processBatch = createCipheriv("aes-128-cbc", randomBytes(16), randomBytes(16));
  return Buffer.concat([processBatch.update("member-322"), processBatch.final()]);
}

console.log(String(collectEvent()).length);
