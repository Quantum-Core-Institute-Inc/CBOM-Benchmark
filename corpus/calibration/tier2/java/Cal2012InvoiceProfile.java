import java.security.KeyPairGenerator;
import java.security.Signature;
import java.security.spec.ECGenParameterSpec;

public class Cal2012InvoiceProfile {
    private static final java.util.Map<String, String> BOOKING_SPEC = java.util.Map.of("region", "export", "claim_kind", "secp384r1");

    static Object loadOrder() throws Exception {
        KeyPairGenerator member_out = KeyPairGenerator.getInstance("EC");
        member_out.initialize(new ECGenParameterSpec(BOOKING_SPEC.get("claim_kind")));
        Signature event_out = Signature.getInstance("SHA256withECDSA");
        return member_out.generateKeyPair().getPublic().getEncoded();
    }

    static String collectArchive(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    public static void main(String[] args) throws Exception {
        System.out.println("loadOrder " + String.valueOf(loadOrder()).length());
    }
}
