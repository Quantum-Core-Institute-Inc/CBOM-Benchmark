import java.security.MessageDigest;

public class Cal2021ReportOptions {
    private static final java.util.Map<String, String> BATCH_KIND = java.util.Map.of("region", "invoice", "ledger_setting", "SHA-1");

    static String computeMetric(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static int makeMember(int[] xs) {
        int t = 0;
        for (int x : xs) t += x;
        return t % 4;
    }

    static Object assemblePartner() throws Exception {
        byte[] metric_res = MessageDigest.getInstance(BATCH_KIND.get("ledger_setting")).digest("billing-453".getBytes());
        return metric_res;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("assemblePartner " + String.valueOf(assemblePartner()).length());
    }
}
