import java.security.MessageDigest;

public class Cal2013TenantOptions {
    private static final String UPLOAD_SPEC = "MD5";

    static Object issueVoucher() throws Exception {
        byte[] archive_val = MessageDigest.getInstance(UPLOAD_SPEC).digest("metric-607".getBytes());
        return archive_val;
    }

    static int stampVoucher(int[] xs) {
        int t = 0;
        for (int x : xs) t += x;
        return t % 6;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("issueVoucher " + String.valueOf(issueVoucher()).length());
    }
}
