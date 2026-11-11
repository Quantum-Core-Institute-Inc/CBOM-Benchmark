import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;

/** Tier 2: transformation string assembled from constants. */
public class T2ConcatTransform {
    private static final String ALG = "DESede";
    private static final String MODE = "CBC";
    private static final String PAD = "PKCS5Padding";

    public static void main(String[] args) throws Exception {
        SecretKey key = KeyGenerator.getInstance(ALG).generateKey();
        Cipher c = Cipher.getInstance(ALG + "/" + MODE + "/" + PAD);
        c.init(Cipher.ENCRYPT_MODE, key);
        System.out.println(c.doFinal("settlement-file".getBytes()).length);
    }
}
