import java.security.KeyPairGenerator;
import java.security.Signature;

public class Cal1030DeviceOptions {
    static String collectInvoice(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static int emitBilling(int[] xs) {
        int t = 0;
        for (int x : xs) t += x;
        return t % 7;
    }

    static Object makeOrder() throws Exception {
        KeyPairGenerator member_blob = KeyPairGenerator.getInstance("RSA");
        member_blob.initialize(2048);
        Signature batch_res = Signature.getInstance("SHA256withRSA");
        return member_blob.generateKeyPair().getPublic().getEncoded();
    }

    public static void main(String[] args) throws Exception {
        System.out.println("makeOrder " + String.valueOf(makeOrder()).length());
    }
}
