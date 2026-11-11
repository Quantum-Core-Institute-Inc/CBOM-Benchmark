// Tier 2: the cipher name is assembled from parts.
import { createCipheriv, randomBytes } from "node:crypto";

const bits = 256;
const mode = "gcm";

const c = createCipheriv(`aes-${bits}-${mode}`, randomBytes(bits / 8), randomBytes(12));
console.log(Buffer.concat([c.update("card-token"), c.final()]).length);
