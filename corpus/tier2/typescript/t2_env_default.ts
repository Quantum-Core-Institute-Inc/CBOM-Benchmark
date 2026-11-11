// Tier 2: modulus size from the environment, with a default.
import { generateKeyPairSync, sign } from "node:crypto";

const KEY_BITS: number = Number(process.env.SIGNING_KEY_BITS ?? 1024);

const { privateKey } = generateKeyPairSync("rsa", { modulusLength: KEY_BITS });
console.log(sign("sha256", Buffer.from("payload"), privateKey).length);
