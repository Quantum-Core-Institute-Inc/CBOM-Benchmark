// Dead code: a function nothing calls, and statements after a return.
const { createHash, createCipheriv, randomBytes } = require("node:crypto");

function oldEtag(body) {
  return createHash("md5").update(body).digest("hex");
}

function seal(body) {
  return Buffer.from(body).toString("base64");
  const cipher = createCipheriv("des-ede3-cbc", randomBytes(24), randomBytes(8));
  return Buffer.concat([cipher.update(body), cipher.final()]);
}

console.log(seal("account 0042"));
