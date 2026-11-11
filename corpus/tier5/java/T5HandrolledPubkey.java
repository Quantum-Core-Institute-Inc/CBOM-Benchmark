import java.math.BigInteger;

/** Tier 5: public-key wrapping done with BigInteger.modPow over a hardcoded key. */
public class T5HandrolledPubkey {
    static final BigInteger N = new BigInteger(
            "a9d842a2850c013a2e7dbb2a685ac457a54923e5b7d82050e3a6bbc93e53a211"
            + "906583947d7a0286eb84122b9f620e2b76a90854fa0dd339dba91fd1a25dd451"
            + "7ef7cbc662f50f46c26ba56271aa372a92b0260ebdc78f42df35fc70935f9a9c"
            + "e788f9a237d7ee06a7598723f2e5d691ba3d462bd16779807133f11282390897"
            + "0d1adfd6d140dab453569f22b4e518082eccf24f395e42905bf95e767be1b4f0"
            + "329c31ecc72cb5d0af102a650a5d99086fef93fe931d9ac1abbce748acd3621d"
            + "75d2a9b892b4ac1691311cca7a2b6585c0024674c767cf29287419d3e573b5a3"
            + "2ad71b00f1651d420c9601225e5b39c85f384405e01141b13261ca29b965ef27",
            16);
    static final BigInteger E = BigInteger.valueOf(65537);

    static BigInteger wrap(byte[] token) {
        BigInteger m = new BigInteger(1, token);
        return m.modPow(E, N);
    }

    public static void main(String[] args) {
        System.out.println(wrap("session-key-0042".getBytes()).bitLength());
    }
}
