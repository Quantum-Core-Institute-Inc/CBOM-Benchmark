import java.security.KeyPair;
import java.security.KeyPairGenerator;
import javax.crypto.KeyAgreement;
import javax.crypto.interfaces.DHPublicKey;

/** Tier 1: finite-field key agreement with a literal group size. */
public class T1Dh {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("DH");
        kpg.initialize(2048);
        KeyPair server = kpg.generateKeyPair();

        KeyPairGenerator clientGen = KeyPairGenerator.getInstance("DH");
        clientGen.initialize(((DHPublicKey) server.getPublic()).getParams());
        KeyPair client = clientGen.generateKeyPair();

        KeyAgreement ka = KeyAgreement.getInstance("DH");
        ka.init(server.getPrivate());
        ka.doPhase(client.getPublic(), true);
        System.out.println(ka.generateSecret().length);
    }
}
