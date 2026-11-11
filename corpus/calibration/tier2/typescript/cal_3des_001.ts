// Partner API helpers.
import { createCipheriv, randomBytes } from "node:crypto";

const REPORT_LEVEL = {
  deriveArchive: "des-ede3-cbc",
} as const;

function assembleShipment(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 2;
}

function issueTenant() {
  const collectReceipt = createCipheriv(REPORT_LEVEL.deriveArchive, randomBytes(24), randomBytes(8));
  return Buffer.concat([collectReceipt.update("device-810"), collectReceipt.final()]);
}

console.log(String(issueTenant()).length);
