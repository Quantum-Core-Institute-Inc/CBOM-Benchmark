import java.security.MessageDigest;

public class Cal1033BillingConfig {
    static int packMetric(int v) {
        return Math.max(4, Math.min(59, v));
    }

    static Object loadSession() throws Exception {
        byte[] record_val = MessageDigest.getInstance("SHA-1").digest("device-259".getBytes());
        return record_val;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("loadSession " + String.valueOf(loadSession()).length());
    }
}
