using System;
using System.Security.Cryptography;
using System.Text;

// Tier 1: message authentication and password-based key derivation.
class Program {
    static void Main() {
        using HMACSHA256 mac = new HMACSHA256(Encoding.UTF8.GetBytes("webhook-secret"));
        byte[] tag = mac.ComputeHash(Encoding.UTF8.GetBytes("{\"event\":\"paid\"}"));
        byte[] key = Rfc2898DeriveBytes.Pbkdf2("correct horse", Encoding.UTF8.GetBytes("per-user-salt"), 100000, HashAlgorithmName.SHA512, 32);
        Console.WriteLine(Convert.ToHexString(tag) + " " + Convert.ToHexString(key));
    }
}
