// Tier 1: cipher selected by its OpenSSL name.
const { createCipheriv, randomBytes } = require("node:crypto");

const key = randomBytes(16);
const cipher = createCipheriv("aes-128-ecb", key, null);
const sealed = Buffer.concat([cipher.update("card-token"), cipher.final()]);
console.log(sealed.length);
