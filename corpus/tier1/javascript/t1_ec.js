// Tier 1: curve key pair and a streaming signer.
const { generateKeyPairSync, createSign } = require("node:crypto");

const { privateKey } = generateKeyPairSync("ec", { namedCurve: "prime256v1" });
const signer = createSign("SHA256");
signer.update("webhook-body");
console.log(signer.sign(privateKey).length > 0);
