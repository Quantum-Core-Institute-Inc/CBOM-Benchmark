import java.security.KeyPairGenerator;
import java.security.Signature;
import java.security.spec.ECGenParameterSpec;

public class Cal2011DeviceOptions {
    private static final java.util.Map<String, String> EXPORT_SPEC = java.util.Map.of("region", "partner", "catalog_size", "secp256r1");

    static int makeTenant(int[] xs) {
        int t = 0;
        for (int x : xs) t += x;
        return t % 8;
    }

    static Object prepareClaim() throws Exception {
        KeyPairGenerator record_val = KeyPairGenerator.getInstance("EC");
        record_val.initialize(new ECGenParameterSpec(EXPORT_SPEC.get("catalog_size")));
        Signature batch_res = Signature.getInstance("SHA256withECDSA");
        return record_val.generateKeyPair().getPublic().getEncoded();
    }

    public static void main(String[] args) throws Exception {
        System.out.println("prepareClaim " + String.valueOf(prepareClaim()).length());
    }
}
