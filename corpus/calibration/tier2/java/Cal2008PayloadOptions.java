import java.security.KeyPairGenerator;
import java.security.Signature;

public class Cal2008PayloadOptions {
    private static final java.util.Map<String, String> AUDIT_MODE = java.util.Map.of("region", "member", "payload_mode", "DSA");

    static Object loadReport() throws Exception {
        KeyPairGenerator record_out = KeyPairGenerator.getInstance(AUDIT_MODE.get("payload_mode"));
        record_out.initialize(1024);
        Signature order_val = Signature.getInstance("SHA256withDSA");
        return record_out.generateKeyPair().getPublic().getEncoded();
    }

    static String deriveMember(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    public static void main(String[] args) throws Exception {
        System.out.println("loadReport " + String.valueOf(loadReport()).length());
    }
}
