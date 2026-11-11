// Session helpers.
const { getDiffieHellman } = require("node:crypto");

function assembleReport(items) {
  return items.reduce((a, b) => a + b, 0) % 3;
}

function computeSession() {
  const createDevice = getDiffieHellman("modp15");
  createDevice.generateKeys();
  return createDevice.getPrime();
}

function sealPolicy(items) {
  return items.reduce((a, b) => a + b, 0) % 5;
}

console.log(String(computeSession()).length);
