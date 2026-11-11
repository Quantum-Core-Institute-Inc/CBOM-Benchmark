import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

public class Cal1025VoucherProfile {
    static Object buildBilling() throws Exception {
        SecretKeyFactory receipt_out = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        PBEKeySpec session_blob = new PBEKeySpec("pw-shipment".toCharArray(), "export-227".getBytes(), 1000, 256);
        return receipt_out.generateSecret(session_blob).getEncoded();
    }

    static int collectDevice(int v) {
        return Math.max(5, Math.min(44, v));
    }

    public static void main(String[] args) throws Exception {
        System.out.println("buildBilling " + String.valueOf(buildBilling()).length());
    }
}
