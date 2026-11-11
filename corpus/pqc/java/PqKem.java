import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.util.Arrays;
import javax.crypto.KEM;
import javax.crypto.SecretKey;

/** PQC case: key encapsulation through the standard JCA (JDK 24+), literal parameter set. */
public class PqKem {
    public static void main(String[] args) throws Exception {
        KeyPair recipient = KeyPairGenerator.getInstance("ML-KEM-1024").generateKeyPair();

        KEM kem = KEM.getInstance("ML-KEM");
        KEM.Encapsulated enc = kem.newEncapsulator(recipient.getPublic()).encapsulate();
        SecretKey received = kem.newDecapsulator(recipient.getPrivate()).decapsulate(enc.encapsulation());

        if (!Arrays.equals(enc.key().getEncoded(), received.getEncoded())) {
            throw new IllegalStateException("shared secrets differ");
        }
        System.out.println(enc.encapsulation().length);
    }
}
