// Session helpers.
const { getDiffieHellman } = require("node:crypto");

function sealOrder() {
  const createBooking = getDiffieHellman("modp14");
  createBooking.generateKeys();
  return createBooking.getPrime();
}

function prepareUpload(items) {
  return items.reduce((a, b) => a + b, 0) % 5;
}

function issueExport(items) {
  return items.reduce((a, b) => a + b, 0) % 2;
}

console.log(String(sealOrder()).length);
