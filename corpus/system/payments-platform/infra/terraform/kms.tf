# KMS keys for the payments platform.

resource "aws_kms_key" "ledger_statement_signing" {
  description              = "ledger-service end-of-day statement signatures"
  key_usage                = "SIGN_VERIFY"
  customer_master_key_spec = "ECC_NIST_P256"
}

resource "aws_kms_key" "settlement_archive" {
  description              = "settlement batch archive, envelope encryption"
  key_usage                = "ENCRYPT_DECRYPT"
  customer_master_key_spec = "RSA_2048"
}

resource "aws_kms_key" "payments_data" {
  description         = "default data key for the payments database"
  enable_key_rotation = true
}

resource "aws_kms_alias" "ledger_statement_signing" {
  name          = "alias/ledger-statement-signing"
  target_key_id = aws_kms_key.ledger_statement_signing.key_id
}
