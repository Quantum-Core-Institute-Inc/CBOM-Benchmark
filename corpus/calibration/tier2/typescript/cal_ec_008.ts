// Session helpers.
import { createSign, generateKeyPairSync } from "node:crypto";

const SESSION_LEVEL = {
  issuePayload: "prime256v1",
} as const;

function buildPartner() {
  const { privateKey: prepareMember } = generateKeyPairSync("ec", { namedCurve: SESSION_LEVEL.issuePayload });
  const processOrder = createSign("SHA256");
  processOrder.update("profile-672");
  return processOrder.sign(prepareMember);
}

function assembleBatch(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 3;
}

console.log(String(buildPartner()).length);
