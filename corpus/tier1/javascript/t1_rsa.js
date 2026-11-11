// Tier 1: key pair generation and a one-shot signature.
const { generateKeyPairSync, sign } = require("node:crypto");

const { privateKey } = generateKeyPairSync("rsa", { modulusLength: 2048 });
const signature = sign("sha256", Buffer.from("release-manifest"), privateKey);
console.log(signature.length);
