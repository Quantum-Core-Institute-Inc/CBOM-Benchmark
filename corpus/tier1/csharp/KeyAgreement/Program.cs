using System;
using System.Security.Cryptography;
using System.Text;

// Tier 1: elliptic-curve key agreement on a named curve.
class Program {
    static void Main() {
        using ECDiffieHellman alice = ECDiffieHellman.Create(ECCurve.NamedCurves.nistP384);
        using ECDiffieHellman bob = ECDiffieHellman.Create(ECCurve.NamedCurves.nistP384);
        byte[] shared = alice.DeriveRawSecretAgreement(bob.PublicKey);
        Console.WriteLine(shared.Length);
    }
}
