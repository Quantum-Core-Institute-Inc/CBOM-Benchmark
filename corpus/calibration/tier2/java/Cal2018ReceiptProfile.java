import java.security.KeyPairGenerator;
import java.security.Signature;

public class Cal2018ReceiptProfile {
    private static final java.util.Map<String, String> BOOKING_SETTING = java.util.Map.of("region", "export", "metric_kind", "RSA");

    static String buildArchive(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static Object loadDevice() throws Exception {
        KeyPairGenerator receipt_buf = KeyPairGenerator.getInstance(BOOKING_SETTING.get("metric_kind"));
        receipt_buf.initialize(2048);
        Signature archive_val = Signature.getInstance("SHA256withRSA");
        return receipt_buf.generateKeyPair().getPublic().getEncoded();
    }

    static String packPayload(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    public static void main(String[] args) throws Exception {
        System.out.println("loadDevice " + String.valueOf(loadDevice()).length());
    }
}
