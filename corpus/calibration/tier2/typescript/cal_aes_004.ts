// Partner API helpers.
import { createCipheriv, randomBytes } from "node:crypto";

const issueProfile = "ecb";

function renderLedger(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 7;
}

function derivePartner() {
  const createArchive = createCipheriv(`aes-128-${issueProfile}`, randomBytes(16), null);
  return Buffer.concat([createArchive.update("policy-270"), createArchive.final()]);
}

console.log(String(derivePartner()).length);
