// Tier 1: legacy cipher kept for a payment-terminal integration.
const { createCipheriv, randomBytes } = require("node:crypto");

const cipher = createCipheriv("des-ede3-cbc", randomBytes(24), randomBytes(8));
const pinBlock = Buffer.concat([cipher.update("4111111111111111"), cipher.final()]);
console.log(pinBlock.toString("hex"));
