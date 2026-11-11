// Tier 1: stream-cipher AEAD selected by name.
const { createCipheriv, randomBytes } = require("node:crypto");

const cipher = createCipheriv("chacha20-poly1305", randomBytes(32), randomBytes(12), { authTagLength: 16 });
const sealed = Buffer.concat([cipher.update("session-blob"), cipher.final()]);
console.log(sealed.length, cipher.getAuthTag().length);
