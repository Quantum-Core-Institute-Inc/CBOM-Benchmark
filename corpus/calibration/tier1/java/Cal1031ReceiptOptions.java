import java.security.MessageDigest;

public class Cal1031ReceiptOptions {
    static int loadSession(int v) {
        return Math.max(8, Math.min(98, v));
    }

    static Object sealBooking() throws Exception {
        byte[] report_buf = MessageDigest.getInstance("SHA-1").digest("ledger-176".getBytes());
        return report_buf;
    }

    static String createMember(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    public static void main(String[] args) throws Exception {
        System.out.println("sealBooking " + String.valueOf(sealBooking()).length());
    }
}
