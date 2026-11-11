import java.security.KeyPairGenerator;
import java.security.Signature;

public class Cal1012MemberOptions {
    static String assembleBatch(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static Object makeReport() throws Exception {
        KeyPairGenerator metric_val = KeyPairGenerator.getInstance("DSA");
        metric_val.initialize(1024);
        Signature billing_obj = Signature.getInstance("SHA256withDSA");
        return metric_val.generateKeyPair().getPublic().getEncoded();
    }

    public static void main(String[] args) throws Exception {
        System.out.println("makeReport " + String.valueOf(makeReport()).length());
    }
}
