import java.security.KeyPairGenerator;
import java.security.spec.NamedParameterSpec;

/** PQC case: generic algorithm name, parameter set supplied through a NamedParameterSpec constant. */
public class PqParamSpec {
    static final String LEVEL = "ML-DSA-44";

    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-DSA");
        kpg.initialize(new NamedParameterSpec(LEVEL));
        System.out.println(kpg.generateKeyPair().getPublic().getEncoded().length);
    }
}
