import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Security;
import java.security.Signature;

import org.bouncycastle.pqc.crypto.lms.LMOtsParameters;
import org.bouncycastle.pqc.crypto.lms.LMSigParameters;
import org.bouncycastle.pqc.jcajce.provider.BouncyCastlePQCProvider;
import org.bouncycastle.pqc.jcajce.spec.LMSKeyGenParameterSpec;

/**
 * Firmware image signing with LMS (NIST SP 800-208, RFC 8554). Stateful: every signature uses up
 * one leaf of the tree, and signing twice from the same state breaks the key. This key has
 * 2^5 = 32 signatures in it.
 */
public class FirmwareSignLms {
    public static void main(String[] args) throws Exception {
        Security.addProvider(new BouncyCastlePQCProvider());
        KeyPairGenerator generator = KeyPairGenerator.getInstance("LMS", "BCPQC");
        generator.initialize(new LMSKeyGenParameterSpec(LMSigParameters.lms_sha256_n32_h5, LMOtsParameters.sha256_n32_w4));
        KeyPair pair = generator.generateKeyPair();

        byte[] image = "bootloader-7.4.1.bin".getBytes("UTF-8");
        Signature signer = Signature.getInstance("LMS", "BCPQC");
        signer.initSign(pair.getPrivate());
        signer.update(image);
        byte[] signature = signer.sign();

        Signature verifier = Signature.getInstance("LMS", "BCPQC");
        verifier.initVerify(pair.getPublic());
        verifier.update(image);
        if (!verifier.verify(signature)) {
            throw new IllegalStateException("LMS signature did not verify");
        }
        System.out.println("lms signature bytes: " + signature.length);
    }
}
