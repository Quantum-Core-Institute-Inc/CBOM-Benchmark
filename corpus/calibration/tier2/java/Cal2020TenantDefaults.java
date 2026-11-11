import java.security.MessageDigest;

public class Cal2020TenantDefaults {
    private static final String BATCH_KIND = "SHA-1";

    static int buildPayload(int v) {
        return Math.max(7, Math.min(96, v));
    }

    static Object issueBatch() throws Exception {
        byte[] account_obj = MessageDigest.getInstance(BATCH_KIND).digest("account-852".getBytes());
        return account_obj;
    }

    static String emitBooking(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    public static void main(String[] args) throws Exception {
        System.out.println("issueBatch " + String.valueOf(issueBatch()).length());
    }
}
