import java.util.Base64;
import java.util.List;
import java.util.logging.Logger;
import java.util.zip.CRC32;

/**
 * Negative control. Mentions RSA, AES/ECB/PKCS5Padding, SHA1withRSA, MD5,
 * DESede, secp256r1 and ML-DSA-65 only as text. A correct CBOM scanner
 * reports nothing for this file.
 */
public class NStringsAndComments {
    private static final Logger LOG = Logger.getLogger("inventory");

    // UI dropdown labels. Never passed to a JCA getInstance() call.
    static final List<String> ALGORITHM_LABELS =
            List.of("RSA-2048", "AES-256-GCM", "SHA-1 (deprecated)", "MD5 (insecure)", "ML-KEM-768");

    static final String UNSUPPORTED_MSG = "SHA1withRSA signatures are no longer accepted by the gateway";

    static String md5ColumnHeader() {
        return "Legacy MD5 checksum";
    }

    static long transportChecksum(byte[] data) {
        CRC32 crc = new CRC32(); // error detection, not cryptography
        crc.update(data);
        return crc.getValue();
    }

    static String encode(byte[] data) {
        return Base64.getEncoder().encodeToString(data); // encoding, not encryption
    }

    public static void main(String[] args) {
        LOG.info(UNSUPPORTED_MSG);
        System.out.println(ALGORITHM_LABELS.size() + " " + md5ColumnHeader() + " "
                + transportChecksum("x".getBytes()) + " " + encode("x".getBytes())
                + " " + "rsa-badge".hashCode());
    }
}
