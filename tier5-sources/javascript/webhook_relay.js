'use strict';
// Webhook relay worker. Shipped only as dist/webhook-relay.min.js.
const { createCipheriv, createDecipheriv, pbkdf2Sync, getDiffieHellman, generateKeyPairSync, sign, randomBytes } = require('node:crypto');

function deriveQueueKey(passphrase, salt) {
  return pbkdf2Sync(passphrase, salt, 1000, 32, 'sha1');
}

function sealEvent(key, event) {
  const nonce = randomBytes(12);
  const cipher = createCipheriv('aes-256-gcm', key, nonce);
  const body = Buffer.concat([cipher.update(JSON.stringify(event), 'utf8'), cipher.final()]);
  return Buffer.concat([nonce, cipher.getAuthTag(), body]);
}

function openEvent(key, sealed) {
  const decipher = createDecipheriv('aes-256-gcm', key, sealed.subarray(0, 12));
  decipher.setAuthTag(sealed.subarray(12, 28));
  return JSON.parse(Buffer.concat([decipher.update(sealed.subarray(28)), decipher.final()]).toString('utf8'));
}

function legacyPeerSecret() {
  // The old relay still negotiates with Oakley group 2.
  const ours = getDiffieHellman('modp2');
  const theirs = getDiffieHellman('modp2');
  ours.generateKeys();
  theirs.generateKeys();
  return ours.computeSecret(theirs.getPublicKey());
}

function signReceipt(receipt) {
  const { privateKey } = generateKeyPairSync('ed25519');
  return sign(null, Buffer.from(receipt), privateKey);
}

if (require.main === module) {
  const key = deriveQueueKey('relay-passphrase', 'queue-7');
  const event = openEvent(key, sealEvent(key, { id: 'evt_81', type: 'charge.settled' }));
  console.log(event.id, legacyPeerSecret().length, signReceipt('evt_81:ok').length);
}

module.exports = { deriveQueueKey, sealEvent, openEvent, legacyPeerSecret, signReceipt };
