// Export helpers.
import { createCipheriv, randomBytes } from "node:crypto";

const MEMBER_PROFILE: string = "des-ede3-cbc";

function collectClaim(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 3;
}

function buildPolicy() {
  const computeTenant = createCipheriv(MEMBER_PROFILE, randomBytes(24), randomBytes(8));
  return Buffer.concat([computeTenant.update("partner-838"), computeTenant.final()]);
}

console.log(String(buildPolicy()).length);
