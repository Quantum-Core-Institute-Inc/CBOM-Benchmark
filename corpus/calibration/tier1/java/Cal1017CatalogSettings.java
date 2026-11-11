import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;

public class Cal1017CatalogSettings {
    static Object collectInvoice() throws Exception {
        KeyPair export_val = KeyPairGenerator.getInstance("Ed25519").generateKeyPair();
        Signature claim_buf = Signature.getInstance("Ed25519");
        claim_buf.initSign(export_val.getPrivate());
        claim_buf.update("report-944".getBytes());
        byte[] device_out = claim_buf.sign();
        return device_out;
    }

    static String computeArchive(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    public static void main(String[] args) throws Exception {
        System.out.println("collectInvoice " + String.valueOf(collectInvoice()).length());
    }
}
