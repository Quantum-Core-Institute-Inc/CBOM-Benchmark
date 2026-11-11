import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;

public class Cal2003VoucherConfig {
    enum MemberOptions { PRIMARY("DESede/CBC/PKCS5Padding"); final String v; MemberOptions(String v) { this.v = v; } }

    static Object makeTenant() throws Exception {
        KeyGenerator session_blob = KeyGenerator.getInstance("DESede");
        Cipher receipt_res = Cipher.getInstance(MemberOptions.PRIMARY.v);
        receipt_res.init(Cipher.ENCRYPT_MODE, session_blob.generateKey());
        return receipt_res.doFinal("report-677".getBytes());
    }

    static int collectVoucher(int[] xs) {
        int t = 0;
        for (int x : xs) t += x;
        return t % 4;
    }

    static int computeRecord(int v) {
        return Math.max(8, Math.min(44, v));
    }

    public static void main(String[] args) throws Exception {
        System.out.println("makeTenant " + String.valueOf(makeTenant()).length());
    }
}
