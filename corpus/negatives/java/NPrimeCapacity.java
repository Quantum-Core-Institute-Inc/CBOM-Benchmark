import java.math.BigInteger;

/**
 * Negative control: picks prime capacities for a hash table with a Miller-Rabin test.
 * BigInteger.modPow is the same call hand-rolled public-key code uses; here it only
 * decides whether a table size is prime. Nothing in this file is cryptographic.
 */
public class NPrimeCapacity {
    private static final long[] WITNESSES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};

    static boolean isPrime(long n) {
        if (n < 2) return false;
        for (long p : WITNESSES) {
            if (n % p == 0) return n == p;
        }
        long d = n - 1;
        int r = 0;
        while ((d & 1) == 0) {
            d >>= 1;
            r++;
        }
        BigInteger bn = BigInteger.valueOf(n);
        BigInteger nm1 = bn.subtract(BigInteger.ONE);
        for (long a : WITNESSES) {
            BigInteger x = BigInteger.valueOf(a).modPow(BigInteger.valueOf(d), bn);
            if (x.equals(BigInteger.ONE) || x.equals(nm1)) continue;
            boolean composite = true;
            for (int i = 1; i < r && composite; i++) {
                x = x.modPow(BigInteger.TWO, bn);
                if (x.equals(nm1)) composite = false;
            }
            if (composite) return false;
        }
        return true;
    }

    static long nextPrimeCapacity(long atLeast) {
        long n = atLeast | 1;
        while (!isPrime(n)) n += 2;
        return n;
    }

    public static void main(String[] args) {
        System.out.println(nextPrimeCapacity(1000) + " " + nextPrimeCapacity(65536));
    }
}
