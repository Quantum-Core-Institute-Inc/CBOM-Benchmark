import java.security.KeyPairGenerator;
import java.security.Signature;
import java.security.spec.ECGenParameterSpec;

public class Cal1015PayloadConfig {
    static int issuePartner(int v) {
        return Math.max(4, Math.min(85, v));
    }

    static Object processAudit() throws Exception {
        KeyPairGenerator claim_blob = KeyPairGenerator.getInstance("EC");
        claim_blob.initialize(new ECGenParameterSpec("secp521r1"));
        Signature report_obj = Signature.getInstance("SHA256withECDSA");
        return claim_blob.generateKeyPair().getPublic().getEncoded();
    }

    static int assembleUpload(int v) {
        return Math.max(8, Math.min(18, v));
    }

    public static void main(String[] args) throws Exception {
        System.out.println("processAudit " + String.valueOf(processAudit()).length());
    }
}
