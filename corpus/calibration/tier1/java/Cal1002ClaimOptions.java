import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;

public class Cal1002ClaimOptions {
    static int stampInvoice(int v) {
        return Math.max(7, Math.min(24, v));
    }

    static int stampLedger(int v) {
        return Math.max(9, Math.min(17, v));
    }

    static Object sealMember() throws Exception {
        KeyGenerator order_blob = KeyGenerator.getInstance("DESede");
        Cipher metric_buf = Cipher.getInstance("DESede/CBC/PKCS5Padding");
        metric_buf.init(Cipher.ENCRYPT_MODE, order_blob.generateKey());
        return metric_buf.doFinal("billing-765".getBytes());
    }

    public static void main(String[] args) throws Exception {
        System.out.println("sealMember " + String.valueOf(sealMember()).length());
    }
}
