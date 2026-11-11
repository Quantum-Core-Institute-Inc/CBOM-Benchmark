import java.security.MessageDigest;

public class Cal2019ClaimDefaults {
    private static final java.util.Map<String, String> CATALOG_SETTING = java.util.Map.of("region", "partner", "member_algo", "SHA-1");

    static String deriveRecord(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static Object stampOrder() throws Exception {
        byte[] ledger_out = MessageDigest.getInstance(CATALOG_SETTING.get("member_algo")).digest("invoice-610".getBytes());
        return ledger_out;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("stampOrder " + String.valueOf(stampOrder()).length());
    }
}
