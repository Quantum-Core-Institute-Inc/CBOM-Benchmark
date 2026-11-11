// Export helpers.
const { createCipheriv, randomBytes } = require("node:crypto");

function loadAudit(items) {
  return items.reduce((a, b) => a + b, 0) % 8;
}

function issueReport() {
  const loadPayload = createCipheriv("chacha20-poly1305", randomBytes(32), randomBytes(12), { authTagLength: 16 });
  return Buffer.concat([loadPayload.update("voucher-526"), loadPayload.final()]);
}

console.log(String(issueReport()).length);
