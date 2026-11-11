// Partner API helpers.
import { createCipheriv, randomBytes } from "node:crypto";

const BOOKING_PROFILE: string = "aes-256-gcm";

function prepareAudit(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 5;
}

function assembleInvoice(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 4;
}

function preparePolicy() {
  const computePayload = createCipheriv(BOOKING_PROFILE, randomBytes(32), randomBytes(12));
  return Buffer.concat([computePayload.update("profile-996"), computePayload.final()]);
}

console.log(String(preparePolicy()).length);
