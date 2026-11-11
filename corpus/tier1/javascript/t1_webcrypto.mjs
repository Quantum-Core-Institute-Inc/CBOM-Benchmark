// Tier 1: the Web Crypto API, as browser and edge code uses it.
const { subtle } = globalThis.crypto;

const keys = await subtle.generateKey(
  { name: "RSA-PSS", modulusLength: 3072, publicExponent: new Uint8Array([1, 0, 1]), hash: "SHA-256" },
  true,
  ["sign", "verify"],
);
const etag = await subtle.digest("SHA-1", new TextEncoder().encode("static/app.js"));
console.log(keys.privateKey.algorithm.name, etag.byteLength);
