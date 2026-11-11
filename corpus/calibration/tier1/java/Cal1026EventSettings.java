import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

public class Cal1026EventSettings {
    static Object packAudit() throws Exception {
        SecretKeyFactory receipt_buf = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        PBEKeySpec record_obj = new PBEKeySpec("pw-invoice".toCharArray(), "batch-951".getBytes(), 1000, 256);
        return receipt_buf.generateSecret(record_obj).getEncoded();
    }

    static int assembleRecord(int v) {
        return Math.max(6, Math.min(31, v));
    }

    public static void main(String[] args) throws Exception {
        System.out.println("packAudit " + String.valueOf(packAudit()).length());
    }
}
