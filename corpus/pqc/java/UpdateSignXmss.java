import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Security;
import java.security.Signature;

import org.bouncycastle.pqc.jcajce.provider.BouncyCastlePQCProvider;
import org.bouncycastle.pqc.jcajce.spec.XMSSParameterSpec;

/**
 * Update-package signing with XMSS (NIST SP 800-208, RFC 8391). Stateful, like LMS: the private
 * key carries a counter and must never be restored from a backup. Tree height 10: 1,024 signatures.
 */
public class UpdateSignXmss {
    public static void main(String[] args) throws Exception {
        Security.addProvider(new BouncyCastlePQCProvider());
        KeyPairGenerator generator = KeyPairGenerator.getInstance("XMSS", "BCPQC");
        generator.initialize(XMSSParameterSpec.SHA2_10_256);
        KeyPair pair = generator.generateKeyPair();

        byte[] manifest = "update-2026.11.manifest".getBytes("UTF-8");
        Signature signer = Signature.getInstance("XMSS", "BCPQC");
        signer.initSign(pair.getPrivate());
        signer.update(manifest);
        byte[] signature = signer.sign();

        Signature verifier = Signature.getInstance("XMSS", "BCPQC");
        verifier.initVerify(pair.getPublic());
        verifier.update(manifest);
        if (!verifier.verify(signature)) {
            throw new IllegalStateException("XMSS signature did not verify");
        }
        System.out.println("xmss signature bytes: " + signature.length);
    }
}
