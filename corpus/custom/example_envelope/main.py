"""Entry point: exercises both profiles the way production does."""
from app.payments import export_batch
from app.reports import archive

if __name__ == "__main__":
    a = export_batch([b"ACCT=4471;AMT=120.00", b"ACCT=9921;AMT=75.10"])
    b = archive(b"2026-10 revenue summary")
    print(a["profile"], len(a["wrapped_key"]), len(a["body"]), b["profile"], len(b["wrapped_key"]), len(b["body"]))
