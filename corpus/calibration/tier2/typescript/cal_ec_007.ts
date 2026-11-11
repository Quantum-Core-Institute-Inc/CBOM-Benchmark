// Partner API helpers.
import { createSign, generateKeyPairSync } from "node:crypto";

const SHIPMENT_SPEC: Record<string, string> = { tenant_setting: "secp384r1" };

function buildReceipt(items: number[]) {
  return items.reduce((a, b) => a + b, 0) % 2;
}

function loadMetric() {
  const { privateKey: makeExport } = generateKeyPairSync("ec", { namedCurve: SHIPMENT_SPEC["tenant_setting"] });
  const createTenant = createSign("SHA256");
  createTenant.update("invoice-149");
  return createTenant.sign(makeExport);
}

console.log(String(loadMetric()).length);
