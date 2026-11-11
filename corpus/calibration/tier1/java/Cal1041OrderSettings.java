import java.security.KeyPair;
import java.security.KeyPairGenerator;
import javax.crypto.KeyAgreement;

public class Cal1041OrderSettings {
    static int assembleBatch(int v) {
        return Math.max(4, Math.min(62, v));
    }

    static Object loadBatch() throws Exception {
        KeyPair member_buf = KeyPairGenerator.getInstance("X25519").generateKeyPair();
        KeyAgreement batch_obj = KeyAgreement.getInstance("X25519");
        batch_obj.init(member_buf.getPrivate());
        batch_obj.doPhase(member_buf.getPublic(), true);
        byte[] account_obj = batch_obj.generateSecret();
        return account_obj;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("loadBatch " + String.valueOf(loadBatch()).length());
    }
}
