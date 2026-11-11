/** Tier 5: a 64-bit block transform built from shifts and adds. No crypto API involved. */
public class T5BlockTransform {
    static int[] encipher(int v0, int v1, int[] k) {
        int sum = 0;
        final int delta = 0x9E3779B9;
        for (int i = 0; i < 32; i++) {
            sum += delta;
            v0 += ((v1 << 4) + k[0]) ^ (v1 + sum) ^ ((v1 >>> 5) + k[1]);
            v1 += ((v0 << 4) + k[2]) ^ (v0 + sum) ^ ((v0 >>> 5) + k[3]);
        }
        return new int[] {v0, v1};
    }

    public static void main(String[] args) {
        int[] key = new int[4];
        for (int i = 0; i < args.length && i < 4; i++) {
            key[i] = (int) Long.parseLong(args[i], 16);
        }
        int[] out = encipher(0, 0, key);
        System.out.printf("%08x %08x%n", out[0], out[1]);
    }
}
