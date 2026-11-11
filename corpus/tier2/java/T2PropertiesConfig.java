import java.io.FileInputStream;
import java.io.InputStream;
import java.nio.file.Path;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.util.Properties;

/** Tier 2: algorithm and key size loaded from a .properties file. */
public class T2PropertiesConfig {
    public static void main(String[] args) throws Exception {
        Path cfg = Path.of(args.length > 0 ? args[0] : "config/crypto.properties");
        Properties props = new Properties();
        try (InputStream in = new FileInputStream(cfg.toFile())) {
            props.load(in);
        }

        KeyPairGenerator kpg = KeyPairGenerator.getInstance(props.getProperty("keypair.algorithm"));
        kpg.initialize(Integer.parseInt(props.getProperty("keypair.size")));
        KeyPair kp = kpg.generateKeyPair();
        System.out.println(kp.getPublic().getAlgorithm());
    }
}
