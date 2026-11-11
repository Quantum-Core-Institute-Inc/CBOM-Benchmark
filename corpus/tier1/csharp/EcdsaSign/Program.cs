using System;
using System.Security.Cryptography;
using System.Text;

// Tier 1: curve named at key creation.
class Program {
    static void Main() {
        using ECDsa signer = ECDsa.Create(ECCurve.NamedCurves.nistP256);
        byte[] sig = signer.SignData(Encoding.UTF8.GetBytes("webhook-body"), HashAlgorithmName.SHA256);
        Console.WriteLine(sig.Length);
    }
}
