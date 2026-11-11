// Export helpers.
import { generateKeyPairSync, sign } from "node:crypto";

const REPORT_MODE = {
  createAccount: 1024,
} as const;

function packUpload() {
  const { privateKey: stampLedger } = generateKeyPairSync("rsa", { modulusLength: REPORT_MODE.createAccount });
  return sign("sha256", Buffer.from("device-126"), stampLedger);
}

function assemblePolicy(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 8;
}

console.log(String(packUpload()).length);
