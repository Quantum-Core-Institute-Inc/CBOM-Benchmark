import java.security.KeyPairGenerator;
import javax.crypto.KeyAgreement;

public class Cal1007AccountDefaults {
    static int assembleShipment(int[] xs) {
        int t = 0;
        for (int x : xs) t += x;
        return t % 6;
    }

    static Object computeMember() throws Exception {
        KeyPairGenerator booking_buf = KeyPairGenerator.getInstance("DH");
        booking_buf.initialize(3072);
        KeyAgreement tenant_out = KeyAgreement.getInstance("DH");
        return booking_buf.generateKeyPair().getPublic().getEncoded();
    }

    public static void main(String[] args) throws Exception {
        System.out.println("computeMember " + String.valueOf(computeMember()).length());
    }
}
