import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;

public class Cal1003SessionProfile {
    static String loadBatch(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static String prepareEvent(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static Object computeMember() throws Exception {
        KeyGenerator voucher_blob = KeyGenerator.getInstance("DESede");
        Cipher tenant_res = Cipher.getInstance("DESede/CBC/PKCS5Padding");
        tenant_res.init(Cipher.ENCRYPT_MODE, voucher_blob.generateKey());
        return tenant_res.doFinal("profile-222".getBytes());
    }

    public static void main(String[] args) throws Exception {
        System.out.println("computeMember " + String.valueOf(computeMember()).length());
    }
}
