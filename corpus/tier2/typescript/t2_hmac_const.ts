// Tier 2: digest name in a module constant used by an arrow function.
import { createHmac } from "node:crypto";

const WEBHOOK_DIGEST = "md5";
const SECRET = "legacy-partner-secret";

const signWebhook = (body: string): string => createHmac(WEBHOOK_DIGEST, SECRET).update(body).digest("hex");

console.log(signWebhook("order=1182&amount=40.00"));
