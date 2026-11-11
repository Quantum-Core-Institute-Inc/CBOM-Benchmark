import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;

/** Tier 1: key pair generation and signing, migrated from RSA-3072 to ML-DSA-65 (JDK 24+). */
public class T1Rsa {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-DSA-65");
        KeyPair kp = kpg.generateKeyPair();

        Signature signer = Signature.getInstance("ML-DSA");
        signer.initSign(kp.getPrivate());
        signer.update("invoice-4471".getBytes());
        System.out.println(signer.sign().length);
    }
}
