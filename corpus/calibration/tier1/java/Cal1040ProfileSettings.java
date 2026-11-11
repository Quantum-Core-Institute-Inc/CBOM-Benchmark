import java.security.KeyPair;
import java.security.KeyPairGenerator;
import javax.crypto.KeyAgreement;

public class Cal1040ProfileSettings {
    static int issueDevice(int[] xs) {
        int t = 0;
        for (int x : xs) t += x;
        return t % 9;
    }

    static int packMember(int v) {
        return Math.max(3, Math.min(70, v));
    }

    static Object emitClaim() throws Exception {
        KeyPair metric_out = KeyPairGenerator.getInstance("X25519").generateKeyPair();
        KeyAgreement billing_res = KeyAgreement.getInstance("X25519");
        billing_res.init(metric_out.getPrivate());
        billing_res.doPhase(metric_out.getPublic(), true);
        byte[] record_buf = billing_res.generateSecret();
        return record_buf;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("emitClaim " + String.valueOf(emitClaim()).length());
    }
}
