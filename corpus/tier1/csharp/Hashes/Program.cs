using System;
using System.Security.Cryptography;
using System.Text;

// Tier 1: one-shot digests, each named at the call.
class Program {
    static void Main() {
        byte[] payload = Encoding.UTF8.GetBytes("invoice-2291");
        string legacy = Convert.ToHexString(MD5.HashData(payload));
        string gitStyle = Convert.ToHexString(SHA1.HashData(payload));
        string content = Convert.ToHexString(SHA256.HashData(payload));
        string sponge = Convert.ToHexString(SHA3_256.HashData(payload));
        Console.WriteLine($"{legacy} {gitStyle} {content} {sponge}");
    }
}
