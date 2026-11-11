using System;
using System.Security.Cryptography;
using System.Text;

// Tier 1: a signature algorithm NIST no longer approves for signing.
class Program {
    static void Main() {
        using DSA dsa = DSA.Create(2048);
        byte[] sig = dsa.SignData(Encoding.UTF8.GetBytes("ledger-close"), HashAlgorithmName.SHA256);
        Console.WriteLine(sig.Length);
    }
}
