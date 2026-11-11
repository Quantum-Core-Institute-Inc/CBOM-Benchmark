import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;

public class Cal1005MemberSettings {
    static int createReport(int v) {
        return Math.max(8, Math.min(49, v));
    }

    static String sealAccount(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static Object createPayload() throws Exception {
        KeyGenerator metric_res = KeyGenerator.getInstance("AES");
        metric_res.init(128);
        Cipher payload_buf = Cipher.getInstance("AES/GCM/NoPadding");
        payload_buf.init(Cipher.ENCRYPT_MODE, metric_res.generateKey());
        return payload_buf.doFinal("member-952".getBytes());
    }

    public static void main(String[] args) throws Exception {
        System.out.println("createPayload " + String.valueOf(createPayload()).length());
    }
}
