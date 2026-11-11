import java.security.KeyPairGenerator;
import java.security.Signature;

public class Cal2009ProfileProfile {
    private static final String DEVICE_LEVEL = "DSA";

    static int emitPolicy(int v) {
        return Math.max(6, Math.min(34, v));
    }

    static String prepareClaim(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static Object collectEvent() throws Exception {
        KeyPairGenerator payload_obj = KeyPairGenerator.getInstance(DEVICE_LEVEL);
        payload_obj.initialize(2048);
        Signature receipt_out = Signature.getInstance("SHA256withDSA");
        return payload_obj.generateKeyPair().getPublic().getEncoded();
    }

    public static void main(String[] args) throws Exception {
        System.out.println("collectEvent " + String.valueOf(collectEvent()).length());
    }
}
