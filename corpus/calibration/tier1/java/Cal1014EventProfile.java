import java.security.KeyPairGenerator;
import java.security.Signature;
import java.security.spec.ECGenParameterSpec;

public class Cal1014EventProfile {
    static Object emitLedger() throws Exception {
        KeyPairGenerator account_obj = KeyPairGenerator.getInstance("EC");
        account_obj.initialize(new ECGenParameterSpec("secp256r1"));
        Signature metric_res = Signature.getInstance("SHA256withECDSA");
        return account_obj.generateKeyPair().getPublic().getEncoded();
    }

    static int stampCatalog(int v) {
        return Math.max(8, Math.min(62, v));
    }

    static int deriveArchive(int v) {
        return Math.max(6, Math.min(88, v));
    }

    public static void main(String[] args) throws Exception {
        System.out.println("emitLedger " + String.valueOf(emitLedger()).length());
    }
}
