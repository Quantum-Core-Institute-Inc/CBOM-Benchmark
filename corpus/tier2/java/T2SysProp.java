import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;

/** Tier 2: transformation from a system property with a hardcoded default. */
public class T2SysProp {
    public static void main(String[] args) throws Exception {
        String transform = System.getProperty("app.cipher", "AES/ECB/PKCS5Padding");
        int keyBits = Integer.getInteger("app.keybits", 128);

        KeyGenerator kg = KeyGenerator.getInstance(transform.split("/")[0]);
        kg.init(keyBits);
        SecretKey key = kg.generateKey();

        Cipher c = Cipher.getInstance(transform);
        c.init(Cipher.ENCRYPT_MODE, key);
        System.out.println(c.doFinal("session-cookie".getBytes()).length);
    }
}
