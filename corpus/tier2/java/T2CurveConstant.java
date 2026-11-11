import java.security.KeyPairGenerator;
import java.security.spec.ECGenParameterSpec;

/** Tier 2: curve name held in a constant. */
public class T2CurveConstant {
    static final String CURVE = "secp384r1";

    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("EC");
        kpg.initialize(new ECGenParameterSpec(CURVE));
        System.out.println(kpg.generateKeyPair().getPublic().getAlgorithm());
    }
}
