import java.security.KeyPairGenerator;
import java.security.Signature;

public class Cal1029MetricOptions {
    static Object renderArchive() throws Exception {
        KeyPairGenerator tenant_obj = KeyPairGenerator.getInstance("RSA");
        tenant_obj.initialize(3072);
        Signature account_out = Signature.getInstance("SHA256withRSA");
        return tenant_obj.generateKeyPair().getPublic().getEncoded();
    }

    static int sealProfile(int v) {
        return Math.max(8, Math.min(66, v));
    }

    public static void main(String[] args) throws Exception {
        System.out.println("renderArchive " + String.valueOf(renderArchive()).length());
    }
}
