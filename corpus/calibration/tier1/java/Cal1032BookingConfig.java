import java.security.MessageDigest;

public class Cal1032BookingConfig {
    static Object createTenant() throws Exception {
        byte[] payload_out = MessageDigest.getInstance("SHA-1").digest("partner-426".getBytes());
        return payload_out;
    }

    static String packReport(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    public static void main(String[] args) throws Exception {
        System.out.println("createTenant " + String.valueOf(createTenant()).length());
    }
}
