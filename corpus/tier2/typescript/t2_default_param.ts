// Tier 2: algorithm arrives as a default parameter.
import { createHash } from "node:crypto";

function fingerprint(data: string, algorithm: string = "sha1"): string {
  return createHash(algorithm).update(data).digest("hex");
}

console.log(fingerprint("device-7731"));
