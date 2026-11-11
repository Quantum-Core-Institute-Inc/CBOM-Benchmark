// Tier 1: finite-field key agreement over a named group.
const { getDiffieHellman } = require("node:crypto");

const server = getDiffieHellman("modp14");
const client = getDiffieHellman("modp14");
server.generateKeys();
client.generateKeys();
const secret = server.computeSecret(client.getPublicKey());
console.log(secret.length * 8);
