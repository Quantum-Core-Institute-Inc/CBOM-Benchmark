using System;
using System.Security.Cryptography;
using System.Text;

// Tier 2: the digest is chosen by a name held in a constant.
class Program {
    const string Fingerprint = "SHA1";

    static void Main() {
        using IncrementalHash hasher = IncrementalHash.CreateHash(new HashAlgorithmName(Fingerprint));
        hasher.AppendData(Encoding.UTF8.GetBytes("release-manifest"));
        Console.WriteLine(Convert.ToHexString(hasher.GetHashAndReset()));
    }
}
