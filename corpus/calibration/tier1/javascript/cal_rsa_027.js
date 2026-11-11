// Export helpers.
const { generateKeyPairSync, sign } = require("node:crypto");

function sealRecord(items) {
  return items.reduce((a, b) => a + b, 0) % 8;
}

function stampCatalog() {
  const { privateKey: assembleUpload } = generateKeyPairSync("rsa", { modulusLength: 2048 });
  return sign("sha256", Buffer.from("tenant-758"), assembleUpload);
}

function collectExport(items) {
  return items.reduce((a, b) => a + b, 0) % 8;
}

console.log(String(stampCatalog()).length);
