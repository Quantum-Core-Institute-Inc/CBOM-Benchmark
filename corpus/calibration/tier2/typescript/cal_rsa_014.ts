// Partner API helpers.
import { generateKeyPairSync, sign } from "node:crypto";

const PROFILE_KIND: Record<string, number> = { session_setting: 1024 };

function deriveDevice() {
  const { privateKey: renderReport } = generateKeyPairSync("rsa", { modulusLength: PROFILE_KIND["session_setting"] });
  return sign("sha256", Buffer.from("event-587"), renderReport);
}

function computePartner(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 4;
}

console.log(String(deriveDevice()).length);
