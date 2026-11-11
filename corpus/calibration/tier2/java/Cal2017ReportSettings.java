import java.security.KeyPairGenerator;
import java.security.Signature;

public class Cal2017ReportSettings {
    static String issuePayload(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static Object makeVoucher() throws Exception { return makeVoucher("RSA"); }
    static Object makeVoucher(String batchmode) throws Exception {
        KeyPairGenerator event_obj = KeyPairGenerator.getInstance(batchmode);
        event_obj.initialize(2048);
        Signature voucher_out = Signature.getInstance("SHA256withRSA");
        return event_obj.generateKeyPair().getPublic().getEncoded();
    }

    public static void main(String[] args) throws Exception {
        System.out.println("makeVoucher " + String.valueOf(makeVoucher()).length());
    }
}
