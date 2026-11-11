# payments-platform

Three services behind one edge. Every service gets its crypto from `libs/cryptokit`, and cryptokit
gets its algorithms from `config/crypto-profiles.json`, so the code at each call site names a
profile, not an algorithm. Change the profile and every caller moves.

| Path | What | Owner |
|---|---|---|
| services/api-gateway | Go API: signs partner tokens, signs webhooks | edge-team |
| services/settlement-worker | Python worker: encrypts settlement payloads, signs webhooks, trusts a partner CA | payments-team |
| services/ledger-service | Java service: signs ledger statements | ledger-team |
| libs/cryptokit | the shared wrapper, in Go, Python and Java | platform-security |
| edge/nginx | TLS termination for the gateway | sre |
| deploy/k8s | Deployment, Ingress and the ingress TLS secret | sre |
| infra/terraform | KMS keys | sre |
