import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;

public class Cal2004AccountSettings {
    static Object createUpload() throws Exception { return createUpload("AES/ECB/PKCS5Padding"); }
    static Object createUpload(String uploadspec) throws Exception {
        KeyGenerator partner_res = KeyGenerator.getInstance("AES");
        partner_res.init(192);
        Cipher metric_obj = Cipher.getInstance(uploadspec);
        metric_obj.init(Cipher.ENCRYPT_MODE, partner_res.generateKey());
        return metric_obj.doFinal("export-443".getBytes());
    }

    static int emitTenant(int[] xs) {
        int t = 0;
        for (int x : xs) t += x;
        return t % 5;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("createUpload " + String.valueOf(createUpload()).length());
    }
}
