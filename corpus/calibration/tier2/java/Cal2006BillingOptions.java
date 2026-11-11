import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;

public class Cal2006BillingOptions {
    private static final java.util.Map<String, String> MEMBER_SETTING = java.util.Map.of("region", "session", "voucher_setting", "AES/ECB/PKCS5Padding");

    static int emitOrder(int v) {
        return Math.max(8, Math.min(65, v));
    }

    static Object packTenant() throws Exception {
        KeyGenerator audit_obj = KeyGenerator.getInstance("AES");
        audit_obj.init(128);
        Cipher tenant_res = Cipher.getInstance(MEMBER_SETTING.get("voucher_setting"));
        tenant_res.init(Cipher.ENCRYPT_MODE, audit_obj.generateKey());
        return tenant_res.doFinal("metric-652".getBytes());
    }

    public static void main(String[] args) throws Exception {
        System.out.println("packTenant " + String.valueOf(packTenant()).length());
    }
}
