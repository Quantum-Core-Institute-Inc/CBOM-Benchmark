using System;
using System.Text;

// Tier 1: the payment-terminal link now hands the block to the HSM service unchanged.
class Program {
    static void Main() {
        byte[] pinBlock = Encoding.UTF8.GetBytes("4111111111111111");
        Console.WriteLine(Convert.ToHexString(pinBlock));
    }
}
