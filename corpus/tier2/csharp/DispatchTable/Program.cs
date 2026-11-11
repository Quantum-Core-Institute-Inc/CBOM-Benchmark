using System;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;

// Tier 2: a table of constructors; which one runs depends on a runtime argument.
class Program {
    static readonly Dictionary<string, Func<HashAlgorithm>> Digests = new Dictionary<string, Func<HashAlgorithm>> {
        ["legacy"] = MD5.Create,
        ["modern"] = SHA512.Create,
    };

    static void Main(string[] args) {
        string choice = args.Length > 0 ? args[0] : "modern";
        using HashAlgorithm digest = Digests[choice]();
        Console.WriteLine(Convert.ToHexString(digest.ComputeHash(Encoding.UTF8.GetBytes("batch-17"))));
    }
}
