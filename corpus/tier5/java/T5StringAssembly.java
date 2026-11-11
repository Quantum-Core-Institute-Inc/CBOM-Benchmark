import java.security.KeyPairGenerator;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;

/** Tier 5: algorithm names built at runtime from reversed strings and char arrays. */
public class T5StringAssembly {
    public static void main(String[] args) throws Exception {
        String kp = new StringBuilder("ASR").reverse().toString();
        KeyPairGenerator kpg = KeyPairGenerator.getInstance(kp);
        kpg.initialize(2048);
        System.out.println(kpg.generateKeyPair().getPublic().getFormat());

        String sym = new String(new char[] {'D', 'E', 'S', 'e', 'd', 'e'});
        Cipher c = Cipher.getInstance(sym + "/" + "CBC" + "/PKCS5Padding");
        c.init(Cipher.ENCRYPT_MODE, KeyGenerator.getInstance(sym).generateKey());
        System.out.println(c.doFinal("settlement".getBytes()).length);
    }
}
