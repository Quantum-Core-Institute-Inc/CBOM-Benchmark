using System;
using System.Collections.Generic;

// Negative control: algorithm names in comments, labels, log text and identifiers.
// The old service used MD5 and 3DES here; both were removed in release 4.2 (see the migration notes).
class Program {
    // Shown in the admin console's "supported algorithms" help panel.
    static readonly Dictionary<string, string> HelpText = new Dictionary<string, string> {
        ["RSA-2048"] = "Legacy partner keys. Not accepted for new integrations.",
        ["AES-256-GCM"] = "Default for data at rest.",
        ["SHA-1"] = "Rejected. Re-issue the certificate.",
    };

    enum RsaPaddingChoice { Unknown, Requested }

    static string Sha256Label(string tenant) {
        return "sha256-report-" + tenant;   // a report name, not a digest
    }

    static void Main() {
        int des = 3;                        // desired shard count
        string ecdsaTicket = "OPS-4471: rotate the ECDSA P-256 signing key";
        Console.WriteLine("TLS 1.0 and TLS 1.1 handshakes are refused at the load balancer.");
        Console.WriteLine($"{HelpText.Count} {Sha256Label("acme")} {des} {ecdsaTicket.Length} {RsaPaddingChoice.Requested}");
    }
}
