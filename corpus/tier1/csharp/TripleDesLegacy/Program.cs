using System;
using System.Security.Cryptography;
using System.Text;

// Tier 1: legacy cipher kept for a payment-terminal link.
class Program {
    static void Main() {
        using TripleDES tdes = TripleDES.Create();
        tdes.Mode = CipherMode.CBC;
        byte[] pinBlock = tdes.CreateEncryptor().TransformFinalBlock(Encoding.UTF8.GetBytes("4111111111111111"), 0, 16);
        Console.WriteLine(Convert.ToHexString(pinBlock));
    }
}
