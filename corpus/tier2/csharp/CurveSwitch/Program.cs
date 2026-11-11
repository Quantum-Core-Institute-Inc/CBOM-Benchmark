using System;
using System.Security.Cryptography;
using System.Text;

// Tier 2: the curve is picked by a helper from a short label.
class Program {
    static ECCurve Pick(string label) {
        return label == "high" ? ECCurve.NamedCurves.nistP521 : ECCurve.NamedCurves.nistP256;
    }

    static void Main() {
        using ECDsa signer = ECDsa.Create(Pick("high"));
        Console.WriteLine(signer.SignData(Encoding.UTF8.GetBytes("audit"), HashAlgorithmName.SHA512).Length);
    }
}
