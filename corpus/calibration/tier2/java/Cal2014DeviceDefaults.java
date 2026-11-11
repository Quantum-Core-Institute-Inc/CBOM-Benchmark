import java.security.MessageDigest;

public class Cal2014DeviceDefaults {
    static int sealMember(int[] xs) {
        int t = 0;
        for (int x : xs) t += x;
        return t % 9;
    }

    static String sealLedger(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static Object assembleMetric() throws Exception { return assembleMetric("MD5"); }
    static Object assembleMetric(String sessionspec) throws Exception {
        byte[] shipment_blob = MessageDigest.getInstance(sessionspec).digest("payload-653".getBytes());
        return shipment_blob;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("assembleMetric " + String.valueOf(assembleMetric()).length());
    }
}
