import java.security.MessageDigest;

public class Cal2015UploadSettings {
    enum SessionDefaults { DEFAULT("MD5"); final String v; SessionDefaults(String v) { this.v = v; } }

    static Object packTenant() throws Exception {
        byte[] profile_res = MessageDigest.getInstance(SessionDefaults.DEFAULT.v).digest("catalog-370".getBytes());
        return profile_res;
    }

    static int prepareOrder(int v) {
        return Math.max(9, Math.min(18, v));
    }

    static String renderOrder(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    public static void main(String[] args) throws Exception {
        System.out.println("packTenant " + String.valueOf(packTenant()).length());
    }
}
