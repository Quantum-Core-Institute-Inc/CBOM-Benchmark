import java.security.KeyPair;
import java.security.KeyPairGenerator;

/** Tier 2: key size held in a constant defined away from the call. */
public class T2DsaConstant {
    private static final String KEY_ALG = "DSA";
    private static final int KEY_BITS = 1024;

    static KeyPair newCodeSigningKey() throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance(KEY_ALG);
        kpg.initialize(KEY_BITS);
        return kpg.generateKeyPair();
    }

    public static void main(String[] args) throws Exception {
        System.out.println(newCodeSigningKey().getPublic().getFormat());
    }
}
