using System;
using System.Security.Cryptography;
using System.Text;

// Tier 2: the key size reaches the constructor through a settings class and a wrapper.
static class Settings {
    public const int SigningBits = 1024;
}

class Program {
    static RSA NewKey(int bits) {
        return RSA.Create(bits);
    }

    static void Main() {
        using RSA rsa = NewKey(Settings.SigningBits);
        byte[] sig = rsa.SignData(Encoding.UTF8.GetBytes("statement"), HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
        Console.WriteLine(sig.Length);
    }
}
