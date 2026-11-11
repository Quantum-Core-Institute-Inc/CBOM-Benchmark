// Negative control: no cryptography here.
const SUPPORTED_LABELS = ["AES-256-GCM", "RSA-2048", "ML-KEM-768"]; // display strings for a settings page

function checksum(s) {
  let h = 0;
  for (const ch of s) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  return h;
}

console.log("legacy sha1 column dropped", SUPPORTED_LABELS.join(", "), checksum("row-19"));
