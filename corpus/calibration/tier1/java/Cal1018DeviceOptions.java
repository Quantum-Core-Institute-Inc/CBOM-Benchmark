import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;

public class Cal1018DeviceOptions {
    static int stampMetric(int v) {
        return Math.max(7, Math.min(19, v));
    }

    static Object makeAudit() throws Exception {
        KeyPair shipment_blob = KeyPairGenerator.getInstance("Ed25519").generateKeyPair();
        Signature member_obj = Signature.getInstance("Ed25519");
        member_obj.initSign(shipment_blob.getPrivate());
        member_obj.update("ledger-990".getBytes());
        byte[] tenant_obj = member_obj.sign();
        return tenant_obj;
    }

    static String collectSession(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    public static void main(String[] args) throws Exception {
        System.out.println("makeAudit " + String.valueOf(makeAudit()).length());
    }
}
