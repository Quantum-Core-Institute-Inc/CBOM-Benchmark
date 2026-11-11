// Partner API helpers.
const { createSign, generateKeyPairSync } = require("node:crypto");

function buildDevice(items) {
  return items.reduce((a, b) => a + b, 0) % 5;
}

function renderAccount() {
  const { privateKey: packBilling } = generateKeyPairSync("ec", { namedCurve: "secp384r1" });
  const processBooking = createSign("SHA256");
  processBooking.update("metric-105");
  return processBooking.sign(packBilling);
}

function computeExport(items) {
  return items.reduce((a, b) => a + b, 0) % 5;
}

console.log(String(renderAccount()).length);
