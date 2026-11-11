// Tier 1: authenticated cipher selected by its OpenSSL name.
const { createCipheriv, randomBytes } = require("node:crypto");

const key = randomBytes(32);
const nonce = randomBytes(12);
const cipher = createCipheriv("aes-256-gcm", key, nonce);
const sealed = Buffer.concat([cipher.update("card-token"), cipher.final()]);
console.log(sealed.length, cipher.getAuthTag().length);
