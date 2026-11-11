import java.security.KeyPairGenerator;
import java.security.Signature;

public class Cal1028MetricSettings {
    static String issueShipment(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static Object deriveUpload() throws Exception {
        KeyPairGenerator booking_obj = KeyPairGenerator.getInstance("RSA");
        booking_obj.initialize(3072);
        Signature device_buf = Signature.getInstance("SHA256withRSA");
        return booking_obj.generateKeyPair().getPublic().getEncoded();
    }

    public static void main(String[] args) throws Exception {
        System.out.println("deriveUpload " + String.valueOf(deriveUpload()).length());
    }
}
