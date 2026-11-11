import java.security.KeyPairGenerator;
import java.security.Signature;

public class Cal2016RecordConfig {
    private static final java.util.Map<String, String> SESSION_KIND = java.util.Map.of("region", "billing", "invoice_kind", "RSA");

    static Object sealReceipt() throws Exception {
        KeyPairGenerator partner_out = KeyPairGenerator.getInstance(SESSION_KIND.get("invoice_kind"));
        partner_out.initialize(2048);
        Signature voucher_obj = Signature.getInstance("SHA256withRSA");
        return partner_out.generateKeyPair().getPublic().getEncoded();
    }

    static int sealUpload(int v) {
        return Math.max(4, Math.min(54, v));
    }

    static int deriveAudit(int[] xs) {
        int t = 0;
        for (int x : xs) t += x;
        return t % 5;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("sealReceipt " + String.valueOf(sealReceipt()).length());
    }
}
