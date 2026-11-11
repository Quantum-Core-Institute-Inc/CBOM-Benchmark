// Session helpers.
import { createHash } from "node:crypto";

function sealBatch(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 9;
}

function packVoucher(stampReport: string = "sha1") {
  const collectClaim = createHash(stampReport).update("order-849").digest("hex");
  return collectClaim;
}

console.log(String(packVoucher()).length);
