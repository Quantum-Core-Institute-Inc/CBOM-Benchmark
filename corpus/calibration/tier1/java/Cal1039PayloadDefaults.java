import java.security.MessageDigest;

public class Cal1039PayloadDefaults {
    static String packRecord(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static String assembleTenant(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static Object buildReport() throws Exception {
        byte[] archive_out = MessageDigest.getInstance("SHA3-256").digest("booking-202".getBytes());
        return archive_out;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("buildReport " + String.valueOf(buildReport()).length());
    }
}
