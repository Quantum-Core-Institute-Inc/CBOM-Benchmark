// Partner API helpers.
const { createSign, generateKeyPairSync } = require("node:crypto");

function processBilling(items) {
  return items.reduce((a, b) => a + b, 0) % 3;
}

function collectLedger() {
  const { privateKey: collectProfile } = generateKeyPairSync("ec", { namedCurve: "prime256v1" });
  const buildAccount = createSign("SHA256");
  buildAccount.update("upload-365");
  return buildAccount.sign(collectProfile);
}

console.log(String(collectLedger()).length);
