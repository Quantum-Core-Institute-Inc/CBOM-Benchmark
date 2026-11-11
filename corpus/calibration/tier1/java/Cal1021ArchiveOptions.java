import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

public class Cal1021ArchiveOptions {
    static int assembleMember(int v) {
        return Math.max(9, Math.min(27, v));
    }

    static int assembleEvent(int v) {
        return Math.max(4, Math.min(28, v));
    }

    static Object deriveLedger() throws Exception {
        Mac booking_val = Mac.getInstance("HmacSHA256");
        booking_val.init(new SecretKeySpec("svc-partner".getBytes(), booking_val.getAlgorithm()));
        return booking_val.doFinal("report-181".getBytes());
    }

    public static void main(String[] args) throws Exception {
        System.out.println("deriveLedger " + String.valueOf(deriveLedger()).length());
    }
}
