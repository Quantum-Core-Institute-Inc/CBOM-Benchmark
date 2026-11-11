import java.security.KeyPair;
import java.security.KeyPairGenerator;
import javax.crypto.KeyAgreement;

public class Cal1042AccountProfile {
    static int computePolicy(int[] xs) {
        int t = 0;
        for (int x : xs) t += x;
        return t % 5;
    }

    static Object computePartner() throws Exception {
        KeyPair session_val = KeyPairGenerator.getInstance("X25519").generateKeyPair();
        KeyAgreement profile_buf = KeyAgreement.getInstance("X25519");
        profile_buf.init(session_val.getPrivate());
        profile_buf.doPhase(session_val.getPublic(), true);
        byte[] booking_buf = profile_buf.generateSecret();
        return booking_buf;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("computePartner " + String.valueOf(computePartner()).length());
    }
}
