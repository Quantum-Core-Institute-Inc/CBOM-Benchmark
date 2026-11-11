import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;

/** Tier 1: key pair generation and signing, literal parameters. */
public class T1Rsa {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA");
        kpg.initialize(3072);
        KeyPair kp = kpg.generateKeyPair();

        Signature signer = Signature.getInstance("SHA256withRSA");
        signer.initSign(kp.getPrivate());
        signer.update("invoice-4471".getBytes());
        System.out.println(signer.sign().length);
    }
}
