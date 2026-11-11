// Tier 2: curve looked up from a profile table.
import { generateKeyPairSync } from "node:crypto";

const CURVES: Record<string, string> = { compat: "secp384r1" };

function keysFor(profile: string) {
  return generateKeyPairSync("ec", { namedCurve: CURVES[profile] });
}

console.log(keysFor("compat").publicKey.asymmetricKeyDetails);
