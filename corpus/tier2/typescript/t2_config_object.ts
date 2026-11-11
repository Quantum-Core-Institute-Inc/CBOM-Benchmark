// Tier 2: cipher name held in a typed configuration object.
import { createCipheriv, randomBytes } from "node:crypto";

const CIPHERS = {
  legacyPinBlock: "des-ede3-cbc",
} as const;

const cipher = createCipheriv(CIPHERS.legacyPinBlock, randomBytes(24), randomBytes(8));
const out: Buffer = Buffer.concat([cipher.update("4111111111111111"), cipher.final()]);
console.log(out.toString("hex"));
