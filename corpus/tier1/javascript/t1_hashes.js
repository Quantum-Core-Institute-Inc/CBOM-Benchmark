// Tier 1: direct digest lookups by name.
const { createHash } = require("node:crypto");

const payload = "invoice-2291";
const legacy = createHash("md5").update(payload).digest("hex");
const gitStyle = createHash("sha1").update(payload).digest("hex");
const content = createHash("sha256").update(payload).digest("hex");
const sponge = createHash("sha3-256").update(payload).digest("hex");
console.log(legacy, gitStyle, content, sponge);
