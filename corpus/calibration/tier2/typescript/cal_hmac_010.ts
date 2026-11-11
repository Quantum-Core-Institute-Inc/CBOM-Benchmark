// Billing helpers.
import { createHmac } from "node:crypto";

const UPLOAD_KIND = {
  stampSession: "md5",
} as const;

function makePayload() {
  const loadBilling = createHmac(UPLOAD_KIND.stampSession, "svc-policy").update("record-874").digest("hex");
  return loadBilling;
}

function collectPartner(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 9;
}

function collectClaim(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 2;
}

console.log(String(makePayload()).length);
