import java.security.MessageDigest;

public class Cal1023AuditProfile {
    static Object prepareMetric() throws Exception {
        byte[] member_val = MessageDigest.getInstance("MD5").digest("claim-690".getBytes());
        return member_val;
    }

    static String buildPayload(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static int buildPolicy(int v) {
        return Math.max(8, Math.min(95, v));
    }

    public static void main(String[] args) throws Exception {
        System.out.println("prepareMetric " + String.valueOf(prepareMetric()).length());
    }
}
