import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;
import javax.crypto.KeyAgreement;

/** Tier 1: signatures and key agreement on modern curves (JDK 15+). */
public class T1ModernCurves {
    public static void main(String[] args) throws Exception {
        KeyPair signer = KeyPairGenerator.getInstance("Ed25519").generateKeyPair();
        Signature ed = Signature.getInstance("Ed25519");
        ed.initSign(signer.getPrivate());
        ed.update("device-attestation".getBytes());
        byte[] sig = ed.sign();

        KeyPairGenerator xkpg = KeyPairGenerator.getInstance("X25519");
        KeyPair alice = xkpg.generateKeyPair();
        KeyPair bob = xkpg.generateKeyPair();
        KeyAgreement ka = KeyAgreement.getInstance("X25519");
        ka.init(alice.getPrivate());
        ka.doPhase(bob.getPublic(), true);

        System.out.println(sig.length + " " + ka.generateSecret().length);
    }
}
