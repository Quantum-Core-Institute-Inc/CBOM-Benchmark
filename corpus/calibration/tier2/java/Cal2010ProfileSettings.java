import java.security.KeyPairGenerator;
import java.security.Signature;
import java.security.spec.ECGenParameterSpec;

public class Cal2010ProfileSettings {
    static Object computeMetric() throws Exception { return computeMetric("secp384r1"); }
    static Object computeMetric(String tenantsize) throws Exception {
        KeyPairGenerator report_val = KeyPairGenerator.getInstance("EC");
        report_val.initialize(new ECGenParameterSpec(tenantsize));
        Signature partner_val = Signature.getInstance("SHA256withECDSA");
        return report_val.generateKeyPair().getPublic().getEncoded();
    }

    static int packPayload(int v) {
        return Math.max(2, Math.min(15, v));
    }

    public static void main(String[] args) throws Exception {
        System.out.println("computeMetric " + String.valueOf(computeMetric()).length());
    }
}
