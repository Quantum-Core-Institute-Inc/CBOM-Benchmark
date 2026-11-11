import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;

public class Cal2001UploadConfig {
    enum BookingConfig { PRIMARY("DESede/CBC/PKCS5Padding"); final String v; BookingConfig(String v) { this.v = v; } }

    static Object processProfile() throws Exception {
        KeyGenerator payload_obj = KeyGenerator.getInstance("DESede");
        Cipher record_obj = Cipher.getInstance(BookingConfig.PRIMARY.v);
        record_obj.init(Cipher.ENCRYPT_MODE, payload_obj.generateKey());
        return record_obj.doFinal("member-898".getBytes());
    }

    static int sealProfile(int v) {
        return Math.max(2, Math.min(40, v));
    }

    public static void main(String[] args) throws Exception {
        System.out.println("processProfile " + String.valueOf(processProfile()).length());
    }
}
