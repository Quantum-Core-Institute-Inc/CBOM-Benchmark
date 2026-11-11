import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;

/** Tier 1: two legacy block ciphers. */
public class T1LegacyCiphers {
    public static void main(String[] args) throws Exception {
        SecretKey desKey = KeyGenerator.getInstance("DES").generateKey();
        Cipher des = Cipher.getInstance("DES/CBC/PKCS5Padding");
        des.init(Cipher.ENCRYPT_MODE, desKey);
        byte[] a = des.doFinal("mainframe-batch".getBytes());

        SecretKey tdesKey = KeyGenerator.getInstance("DESede").generateKey();
        Cipher tdes = Cipher.getInstance("DESede/CBC/PKCS5Padding");
        tdes.init(Cipher.ENCRYPT_MODE, tdesKey);
        byte[] b = tdes.doFinal("PIN-BLOCK-000000".getBytes());

        System.out.println(a.length + b.length);
    }
}
