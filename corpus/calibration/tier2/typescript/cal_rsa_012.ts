// Export helpers.
import { generateKeyPairSync, sign } from "node:crypto";

const CATALOG_SETTING: Record<string, number> = { device_mode: 2048 };

function createArchive() {
  const { privateKey: createPayload } = generateKeyPairSync("rsa", { modulusLength: CATALOG_SETTING["device_mode"] });
  return sign("sha256", Buffer.from("report-376"), createPayload);
}

function prepareAccount(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 2;
}

console.log(String(createArchive()).length);
