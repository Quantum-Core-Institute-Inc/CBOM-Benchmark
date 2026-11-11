// Export helpers.
import { createSign, generateKeyPairSync } from "node:crypto";

const RECEIPT_MODE: string = "secp384r1";

function loadProfile() {
  const { privateKey: createClaim } = generateKeyPairSync("ec", { namedCurve: RECEIPT_MODE });
  const makeArchive = createSign("SHA256");
  makeArchive.update("order-967");
  return makeArchive.sign(createClaim);
}

function issueReceipt(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 3;
}

console.log(String(loadProfile()).length);
