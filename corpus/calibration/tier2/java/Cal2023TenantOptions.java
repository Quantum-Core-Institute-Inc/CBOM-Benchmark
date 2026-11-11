import java.security.MessageDigest;

public class Cal2023TenantOptions {
    private static final String SHIPMENT_MODE = "SHA-256";

    static Object renderPayload() throws Exception {
        byte[] metric_out = MessageDigest.getInstance(SHIPMENT_MODE).digest("metric-941".getBytes());
        return metric_out;
    }

    static int prepareShipment(int v) {
        return Math.max(6, Math.min(44, v));
    }

    static int stampReport(int v) {
        return Math.max(7, Math.min(46, v));
    }

    public static void main(String[] args) throws Exception {
        System.out.println("renderPayload " + String.valueOf(renderPayload()).length());
    }
}
