import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;

public class Cal2002VoucherDefaults {
    private static final String BATCH_MODE = "DESede/CBC/PKCS5Padding";

    static int sealExport(int[] xs) {
        int t = 0;
        for (int x : xs) t += x;
        return t % 8;
    }

    static Object sealSession() throws Exception {
        KeyGenerator policy_val = KeyGenerator.getInstance("DESede");
        Cipher account_blob = Cipher.getInstance(BATCH_MODE);
        account_blob.init(Cipher.ENCRYPT_MODE, policy_val.generateKey());
        return account_blob.doFinal("invoice-102".getBytes());
    }

    public static void main(String[] args) throws Exception {
        System.out.println("sealSession " + String.valueOf(sealSession()).length());
    }
}
