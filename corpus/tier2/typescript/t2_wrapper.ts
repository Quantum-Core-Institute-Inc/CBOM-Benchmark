// Tier 2: a generic helper; the caller names the cipher.
import { createCipheriv, randomBytes } from "node:crypto";

function seal(algorithm: string, key: Buffer, data: string): Buffer {
  const c = createCipheriv(algorithm, key, null);
  return Buffer.concat([c.update(data), c.final()]);
}

console.log(seal("aes-128-ecb", randomBytes(16), "export row 19").toString("hex"));
