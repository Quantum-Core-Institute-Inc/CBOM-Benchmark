import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

public class Cal1020BookingConfig {
    static Object renderPayload() throws Exception {
        Mac voucher_buf = Mac.getInstance("HmacSHA256");
        voucher_buf.init(new SecretKeySpec("svc-upload".getBytes(), voucher_buf.getAlgorithm()));
        return voucher_buf.doFinal("device-310".getBytes());
    }

    static String makeBooking(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static String deriveArchive(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    public static void main(String[] args) throws Exception {
        System.out.println("renderPayload " + String.valueOf(renderPayload()).length());
    }
}
