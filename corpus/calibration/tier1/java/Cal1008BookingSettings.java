import java.security.KeyPairGenerator;
import javax.crypto.KeyAgreement;

public class Cal1008BookingSettings {
    static String buildPayload(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static String processReport(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static Object collectBatch() throws Exception {
        KeyPairGenerator session_blob = KeyPairGenerator.getInstance("DH");
        session_blob.initialize(3072);
        KeyAgreement batch_obj = KeyAgreement.getInstance("DH");
        return session_blob.generateKeyPair().getPublic().getEncoded();
    }

    public static void main(String[] args) throws Exception {
        System.out.println("collectBatch " + String.valueOf(collectBatch()).length());
    }
}
