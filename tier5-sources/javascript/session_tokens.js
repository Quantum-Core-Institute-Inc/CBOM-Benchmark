'use strict';
// Session token service. Shipped to production only as dist/session-tokens.min.js.
const crypto = require('node:crypto');

const CACHE_DIGEST = 'md5';
const COOKIE_CIPHER = 'aes-128-cbc';
const ISSUER_BITS = 1024;

function cacheKey(userId, route) {
  return crypto.createHash(CACHE_DIGEST).update(`${userId}:${route}`).digest('hex');
}

function sealCookie(key, payload) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(COOKIE_CIPHER, key, iv);
  return Buffer.concat([iv, cipher.update(JSON.stringify(payload), 'utf8'), cipher.final()]).toString('base64url');
}

function openCookie(key, sealed) {
  const raw = Buffer.from(sealed, 'base64url');
  const decipher = crypto.createDecipheriv(COOKIE_CIPHER, key, raw.subarray(0, 16));
  return JSON.parse(Buffer.concat([decipher.update(raw.subarray(16)), decipher.final()]).toString('utf8'));
}

function newIssuerKey() {
  return crypto.generateKeyPairSync('rsa', { modulusLength: ISSUER_BITS });
}

function signToken(privateKey, claims) {
  const body = Buffer.from(JSON.stringify(claims)).toString('base64url');
  const signature = crypto.sign('sha256', Buffer.from(body), privateKey).toString('base64url');
  return `${body}.${signature}`;
}

if (require.main === module) {
  const key = crypto.randomBytes(16);
  const sealed = sealCookie(key, { sid: 'a81f', exp: 1790000000 });
  if (openCookie(key, sealed).sid !== 'a81f') throw new Error('cookie round trip failed');
  const { privateKey } = newIssuerKey();
  const token = signToken(privateKey, { sub: 'u-204' });
  console.log(cacheKey('u-204', '/orders').length, sealed.length > 0, token.split('.').length);
}

module.exports = { cacheKey, sealCookie, openCookie, newIssuerKey, signToken };
