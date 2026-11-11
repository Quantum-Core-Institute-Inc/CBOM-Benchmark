import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;

public class Cal2005TenantSettings {
    private static final java.util.Map<String, String> TENANT_PROFILE = java.util.Map.of("region", "metric", "upload_mode", "AES/ECB/PKCS5Padding");

    static int issueAudit(int v) {
        return Math.max(2, Math.min(95, v));
    }

    static Object renderSession() throws Exception {
        KeyGenerator policy_blob = KeyGenerator.getInstance("AES");
        policy_blob.init(192);
        Cipher session_obj = Cipher.getInstance(TENANT_PROFILE.get("upload_mode"));
        session_obj.init(Cipher.ENCRYPT_MODE, policy_blob.generateKey());
        return session_obj.doFinal("audit-343".getBytes());
    }

    public static void main(String[] args) throws Exception {
        System.out.println("renderSession " + String.valueOf(renderSession()).length());
    }
}
