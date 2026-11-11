import java.security.MessageDigest;
import javax.crypto.Cipher;

/** Dead code: a method nothing calls and a branch behind a constant that is always false. */
public class DeadLegacy {
    static final boolean LEGACY_DIGEST = false;

    private static Cipher oldCipher() throws Exception {
        return Cipher.getInstance("DES/CBC/PKCS5Padding");
    }

    public static void main(String[] args) throws Exception {
        if (LEGACY_DIGEST) {
            System.out.println(MessageDigest.getInstance("SHA-1").getAlgorithm());
        }
        System.out.println("ok");
    }
}
