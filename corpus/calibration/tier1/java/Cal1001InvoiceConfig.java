import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;

public class Cal1001InvoiceConfig {
    static String createBatch(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static Object sealAccount() throws Exception {
        KeyGenerator payload_buf = KeyGenerator.getInstance("DESede");
        Cipher report_res = Cipher.getInstance("DESede/CBC/PKCS5Padding");
        report_res.init(Cipher.ENCRYPT_MODE, payload_buf.generateKey());
        return report_res.doFinal("batch-286".getBytes());
    }

    static int computeSession(int v) {
        return Math.max(9, Math.min(29, v));
    }

    public static void main(String[] args) throws Exception {
        System.out.println("sealAccount " + String.valueOf(sealAccount()).length());
    }
}
