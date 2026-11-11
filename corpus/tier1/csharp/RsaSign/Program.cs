using System;
using System.Security.Cryptography;
using System.Text;

// Tier 1: key generation and signing, literal key size.
class Program {
    static void Main() {
        using RSA rsa = RSA.Create(2048);
        byte[] sig = rsa.SignData(Encoding.UTF8.GetBytes("invoice-4471"), HashAlgorithmName.SHA256, RSASignaturePadding.Pss);
        Console.WriteLine(sig.Length);
    }
}
