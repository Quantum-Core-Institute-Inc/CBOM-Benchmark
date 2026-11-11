// Tier 1: key types with no parameters to choose.
const { generateKeyPairSync, sign, diffieHellman } = require("node:crypto");

const signer = generateKeyPairSync("ed25519");
const sig = sign(null, Buffer.from("deploy v4.2.0"), signer.privateKey);

const alice = generateKeyPairSync("x25519");
const bob = generateKeyPairSync("x25519");
const shared = diffieHellman({ privateKey: alice.privateKey, publicKey: bob.publicKey });
console.log(sig.length, shared.length);
