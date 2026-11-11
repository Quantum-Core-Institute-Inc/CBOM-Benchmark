import java.security.KeyPairGenerator;
import java.security.Signature;

public class Cal2007PayloadDefaults {
    static Object buildExport() throws Exception { return buildExport("DSA"); }
    static Object buildExport(String shipmentspec) throws Exception {
        KeyPairGenerator batch_val = KeyPairGenerator.getInstance(shipmentspec);
        batch_val.initialize(2048);
        Signature account_val = Signature.getInstance("SHA256withDSA");
        return batch_val.generateKeyPair().getPublic().getEncoded();
    }

    static int computeDevice(int v) {
        return Math.max(9, Math.min(61, v));
    }

    public static void main(String[] args) throws Exception {
        System.out.println("buildExport " + String.valueOf(buildExport()).length());
    }
}
