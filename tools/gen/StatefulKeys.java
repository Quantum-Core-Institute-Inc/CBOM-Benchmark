import java.nio.file.Files;
import java.nio.file.Path;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Security;
import java.util.Base64;

import org.bouncycastle.pqc.crypto.lms.LMOtsParameters;
import org.bouncycastle.pqc.crypto.lms.LMSigParameters;
import org.bouncycastle.pqc.jcajce.provider.BouncyCastlePQCProvider;
import org.bouncycastle.pqc.jcajce.spec.LMSKeyGenParameterSpec;
import org.bouncycastle.pqc.jcajce.spec.XMSSParameterSpec;

/**
 * Writes the two stateful hash-based public keys under corpus/pqc/assets/keys (SPKI PEM).
 * Only the public halves are written: a stateful private key in a repository is the mistake
 * these schemes can't survive. Needs Bouncy Castle (bcprov) on the classpath.
 *
 *   javac -cp /usr/share/java/bcprov.jar -d /tmp/gen tools/gen/StatefulKeys.java
 *   java  -cp /tmp/gen:/usr/share/java/bcprov.jar StatefulKeys corpus/pqc/assets/keys
 */
public class StatefulKeys {
    static void pem(Path out, byte[] spki) throws Exception {
        String body = Base64.getMimeEncoder(64, "\n".getBytes()).encodeToString(spki);
        Files.writeString(out, "-----BEGIN PUBLIC KEY-----\n" + body + "\n-----END PUBLIC KEY-----\n");
    }

    public static void main(String[] args) throws Exception {
        Path dir = Path.of(args[0]);
        Security.addProvider(new BouncyCastlePQCProvider());

        KeyPairGenerator lms = KeyPairGenerator.getInstance("LMS", "BCPQC");
        lms.initialize(new LMSKeyGenParameterSpec(LMSigParameters.lms_sha256_n32_h10, LMOtsParameters.sha256_n32_w8));
        KeyPair a = lms.generateKeyPair();
        pem(dir.resolve("bootloader_lms_pub.pem"), a.getPublic().getEncoded());

        KeyPairGenerator xmss = KeyPairGenerator.getInstance("XMSS", "BCPQC");
        xmss.initialize(XMSSParameterSpec.SHA2_10_256);
        KeyPair b = xmss.generateKeyPair();
        pem(dir.resolve("update_xmss_pub.pem"), b.getPublic().getEncoded());
    }
}
