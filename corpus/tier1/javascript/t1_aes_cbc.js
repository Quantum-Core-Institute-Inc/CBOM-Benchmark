// Tier 1: cipher selected by its OpenSSL name.
const { createCipheriv, randomBytes } = require("node:crypto");

const key = randomBytes(16);
const iv = randomBytes(16);
const cipher = createCipheriv("aes-128-cbc", key, iv);
const out = Buffer.concat([cipher.update("account 0042"), cipher.final()]);
console.log(out.toString("hex"));
