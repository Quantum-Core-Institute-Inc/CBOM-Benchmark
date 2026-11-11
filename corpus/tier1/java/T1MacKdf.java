import java.security.SecureRandom;
import javax.crypto.Mac;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;

/** Tier 1: message authentication and password-based key derivation. */
public class T1MacKdf {
    public static void main(String[] args) throws Exception {
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec("shared-webhook-secret".getBytes(), "HmacSHA256"));
        byte[] tag = mac.doFinal("{\"event\":\"paid\"}".getBytes());

        byte[] salt = new byte[16];
        new SecureRandom().nextBytes(salt);
        SecretKeyFactory skf = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        byte[] derived = skf.generateSecret(
                new PBEKeySpec("correct horse battery staple".toCharArray(), salt, 600_000, 256)).getEncoded();

        System.out.println(tag.length + " " + derived.length);
    }
}
