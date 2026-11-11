import java.security.MessageDigest;

public class Cal1034ProfileDefaults {
    static int makeReport(int[] xs) {
        int t = 0;
        for (int x : xs) t += x;
        return t % 5;
    }

    static Object createAccount() throws Exception {
        byte[] receipt_blob = MessageDigest.getInstance("SHA-256").digest("booking-285".getBytes());
        return receipt_blob;
    }

    static int prepareVoucher(int v) {
        return Math.max(3, Math.min(46, v));
    }

    public static void main(String[] args) throws Exception {
        System.out.println("createAccount " + String.valueOf(createAccount()).length());
    }
}
