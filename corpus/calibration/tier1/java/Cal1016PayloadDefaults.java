import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;

public class Cal1016PayloadDefaults {
    static String assembleLedger(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static Object assembleMember() throws Exception {
        KeyPair member_buf = KeyPairGenerator.getInstance("Ed25519").generateKeyPair();
        Signature shipment_val = Signature.getInstance("Ed25519");
        shipment_val.initSign(member_buf.getPrivate());
        shipment_val.update("receipt-189".getBytes());
        byte[] member_blob = shipment_val.sign();
        return member_blob;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("assembleMember " + String.valueOf(assembleMember()).length());
    }
}
