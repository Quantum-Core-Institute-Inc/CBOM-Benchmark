import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;

/** PQC case: signing through the standard JCA (JDK 24+), literal parameter set. */
public class PqSignature {
    public static void main(String[] args) throws Exception {
        KeyPair kp = KeyPairGenerator.getInstance("ML-DSA-87").generateKeyPair();
        byte[] firmware = "bootloader-v7.bin".getBytes();

        Signature s = Signature.getInstance("ML-DSA");
        s.initSign(kp.getPrivate());
        s.update(firmware);
        byte[] sig = s.sign();

        s.initVerify(kp.getPublic());
        s.update(firmware);
        System.out.println(sig.length + " " + s.verify(sig));
    }
}
