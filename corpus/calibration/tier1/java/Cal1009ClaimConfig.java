import java.security.KeyPairGenerator;
import javax.crypto.KeyAgreement;

public class Cal1009ClaimConfig {
    static int emitMember(int v) {
        return Math.max(9, Math.min(81, v));
    }

    static Object emitAudit() throws Exception {
        KeyPairGenerator partner_res = KeyPairGenerator.getInstance("DH");
        partner_res.initialize(2048);
        KeyAgreement batch_res = KeyAgreement.getInstance("DH");
        return partner_res.generateKeyPair().getPublic().getEncoded();
    }

    static String collectOrder(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    public static void main(String[] args) throws Exception {
        System.out.println("emitAudit " + String.valueOf(emitAudit()).length());
    }
}
