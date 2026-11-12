'use strict';
// Partner payments SDK. Shipped to integrators only as dist/payments-sdk.min.js.
const crypto = require('node:crypto');

const ALGORITHMS = {
  fingerprint: 'sha1',
  requestMac: 'md5',
  pinBlock: 'des-ede3-cbc',
  deviceCurve: 'prime256v1',
};

function merchantFingerprint(merchantId, terminalId) {
  return crypto.createHash(ALGORITHMS.fingerprint).update(`${merchantId}|${terminalId}`).digest('hex');
}

function signRequest(sharedKey, method, path, body) {
  return crypto.createHmac(ALGORITHMS.requestMac, sharedKey).update([method, path, body].join('\n')).digest('base64');
}

function sealPinBlock(key, pinBlock) {
  const iv = crypto.randomBytes(8);
  const cipher = crypto.createCipheriv(ALGORITHMS.pinBlock, key, iv);
  return Buffer.concat([iv, cipher.update(pinBlock), cipher.final()]);
}

function newDeviceKey() {
  return crypto.generateKeyPairSync('ec', { namedCurve: ALGORITHMS.deviceCurve });
}

if (require.main === module) {
  const sealed = sealPinBlock(crypto.randomBytes(24), Buffer.from('0412AC89ABCDEF67', 'hex'));
  const { publicKey } = newDeviceKey();
  console.log(merchantFingerprint('m-204', 't-9').length, signRequest('k', 'POST', '/v1/charges', '{}').length,
    sealed.length, publicKey.asymmetricKeyDetails.namedCurve);
}

module.exports = { merchantFingerprint, signRequest, sealPinBlock, newDeviceKey };
