import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;
import java.security.spec.ECGenParameterSpec;

/** Tier 1: key pair generation and signing, literal parameters. */
public class T1Ecdsa {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("EC");
        kpg.initialize(new ECGenParameterSpec("secp256r1"));
        KeyPair kp = kpg.generateKeyPair();

        Signature ecdsa = Signature.getInstance("SHA256withECDSA");
        ecdsa.initSign(kp.getPrivate());
        ecdsa.update("telemetry-batch-9".getBytes());
        System.out.println(ecdsa.sign().length);
    }
}
