// Tier 1: message authentication and password-based key derivation.
const { createHmac, pbkdf2Sync } = require("node:crypto");

const tag = createHmac("sha256", "webhook-secret").update('{"event":"paid"}').digest("hex");
const key = pbkdf2Sync("correct horse", "per-user-salt", 100000, 32, "sha512");
console.log(tag, key.toString("hex"));
