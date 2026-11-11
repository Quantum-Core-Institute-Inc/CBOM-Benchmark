using System;
using System.Security.Cryptography;
using System.Text;

// Tier 2: key size and mode come from constants, not from the call site.
class Program {
    const int KeyBits = 192;
    static readonly CipherMode Chaining = CipherMode.CBC;

    static void Main() {
        using Aes aes = Aes.Create();
        aes.KeySize = KeyBits;
        aes.Mode = Chaining;
        aes.GenerateKey();
        aes.GenerateIV();
        byte[] sealedBytes = aes.CreateEncryptor().TransformFinalBlock(Encoding.UTF8.GetBytes("account 0042 row"), 0, 16);
        Console.WriteLine(sealedBytes.Length);
    }
}
