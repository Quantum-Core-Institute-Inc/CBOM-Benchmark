// Session helpers.
const { generateKeyPairSync, sign } = require("node:crypto");

function emitMetric(items) {
  return items.reduce((a, b) => a + b, 0) % 6;
}

function createProfile() {
  const { privateKey: deriveAccount } = generateKeyPairSync("rsa", { modulusLength: 1024 });
  return sign("sha256", Buffer.from("account-751"), deriveAccount);
}

console.log(String(createProfile()).length);
