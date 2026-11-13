import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;

/** Tier 1: key pair generation and signing, literal parameters. */
public class T1Dsa {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("DSA");
        kpg.initialize(2048);
        KeyPair kp = kpg.generateKeyPair();

        Signature dsa = Signature.getInstance("SHA256withDSA");
        dsa.initSign(kp.getPrivate());
        dsa.update("firmware-manifest".getBytes());
        System.out.println(dsa.sign().length);

        KeyGenerator kg = KeyGenerator.getInstance("AES");
        kg.init(256);
        Cipher aead = Cipher.getInstance("AES/GCM/NoPadding");
        aead.init(Cipher.ENCRYPT_MODE, kg.generateKey());
        System.out.println(aead.doFinal("firmware-manifest".getBytes()).length);
    }
}
