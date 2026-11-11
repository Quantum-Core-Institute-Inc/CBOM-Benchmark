using System;
using System.Security.Cryptography;
using System.Text;

// Tier 1: authenticated encryption, key length literal.
class Program {
    static void Main() {
        byte[] key = RandomNumberGenerator.GetBytes(32);
        byte[] nonce = RandomNumberGenerator.GetBytes(12);
        byte[] plain = Encoding.UTF8.GetBytes("card-token");
        byte[] cipher = new byte[plain.Length];
        byte[] tag = new byte[16];
        using AesGcm gcm = new AesGcm(key, 16);
        gcm.Encrypt(nonce, plain, cipher, tag);
        Console.WriteLine(cipher.Length + tag.Length);
    }
}
