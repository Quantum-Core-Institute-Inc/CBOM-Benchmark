import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;

/** Tier 1: key pair generation and signing, literal parameters. */
public class T1Dsa {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("DSA");
        kpg.initialize(2048);
        KeyPair kp = kpg.generateKeyPair();

        Signature dsa = Signature.getInstance("SHA256withDSA");
        dsa.initSign(kp.getPrivate());
        dsa.update("firmware-manifest".getBytes());
        System.out.println(dsa.sign().length);
    }
}
