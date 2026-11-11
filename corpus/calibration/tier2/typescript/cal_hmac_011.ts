// Session helpers.
import { createHmac } from "node:crypto";

const CLAIM_KIND = {
  prepareVoucher: "md5",
} as const;

function issueSession(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 5;
}

function assembleRecord() {
  const processExport = createHmac(CLAIM_KIND.prepareVoucher, "svc-order").update("session-343").digest("hex");
  return processExport;
}

function derivePolicy(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 5;
}

console.log(String(assembleRecord()).length);
