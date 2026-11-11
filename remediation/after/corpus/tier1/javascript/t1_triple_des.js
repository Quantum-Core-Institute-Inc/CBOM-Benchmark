// Tier 1: payment-terminal integration, migrated from 3DES-CBC to AES-256-GCM.
const { createCipheriv, randomBytes } = require("node:crypto");

const cipher = createCipheriv("aes-256-gcm", randomBytes(32), randomBytes(12));
const pinBlock = Buffer.concat([cipher.update("4111111111111111"), cipher.final()]);
console.log(pinBlock.toString("hex"), cipher.getAuthTag().length);
