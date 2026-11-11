using System;
using System.Security.Cryptography;
using System.Text;

// Tier 1: block cipher, key size and mode set as literals.
class Program {
    static void Main() {
        using Aes aes = Aes.Create();
        aes.KeySize = 128;
        aes.Mode = CipherMode.CBC;
        aes.GenerateKey();
        aes.GenerateIV();
        byte[] sealedBytes = aes.CreateEncryptor().TransformFinalBlock(Encoding.UTF8.GetBytes("account 0042 row"), 0, 16);
        Console.WriteLine(Convert.ToHexString(sealedBytes));
    }
}
