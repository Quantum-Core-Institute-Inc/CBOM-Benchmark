import java.security.MessageDigest;

public class Cal2024TenantSettings {
    private static final String SHIPMENT_SETTING = "SHA-256";

    static int computeVoucher(int v) {
        return Math.max(6, Math.min(17, v));
    }

    static Object assembleBilling() throws Exception {
        byte[] export_val = MessageDigest.getInstance(SHIPMENT_SETTING).digest("export-801".getBytes());
        return export_val;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("assembleBilling " + String.valueOf(assembleBilling()).length());
    }
}
