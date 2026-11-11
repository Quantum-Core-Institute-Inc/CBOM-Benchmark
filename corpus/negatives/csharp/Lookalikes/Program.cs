using System;
using System.Collections.Generic;
using System.Text;

// Negative control: checksums, encodings and hash-table hashing. Nothing cryptographic.
class Program {
    static uint Crc32(byte[] data) {
        uint crc = 0xFFFFFFFF;
        foreach (byte b in data) {
            crc ^= b;
            for (int i = 0; i < 8; i++) {
                crc = (crc & 1) != 0 ? (crc >> 1) ^ 0xEDB88320 : crc >> 1;
            }
        }
        return ~crc;
    }

    static uint Fnv1a(string text) {
        uint hash = 2166136261;
        foreach (char c in text) {
            hash = (hash ^ c) * 16777619;
        }
        return hash;
    }

    static void Main() {
        byte[] payload = Encoding.UTF8.GetBytes("shipment-7731");
        var buckets = new Dictionary<int, string> { [HashCode.Combine("eu-west", 7731)] = "shard-3" };
        string encoded = Convert.ToBase64String(payload);
        Guid requestId = Guid.NewGuid();
        var jitter = new Random(42).Next(0, 250);
        Console.WriteLine($"{Crc32(payload):X8} {Fnv1a("shipment-7731"):X8} {encoded} {buckets.Count} {requestId.ToString().Length} {jitter >= 0}");
    }
}
