import java.util.zip.Adler32;

/** Negative control: identifiers and types that look like crypto but are not. */
public class NLookalikes {
    /** Renders the amber "RSA" badge next to legacy certificates. Pure UI. */
    static class RsaBadgeRenderer {
        String html() {
            return "<span class=\"badge\">RSA</span>";
        }
    }

    enum CipherSuiteLabel { TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_AES_256_GCM_SHA384 }

    static final String SHA256_OF_EMPTY =
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855";

    static long fastHash(byte[] data) {
        Adler32 a = new Adler32();
        a.update(data);
        return a.getValue();
    }

    public static void main(String[] args) {
        System.out.println(new RsaBadgeRenderer().html() + " "
                + CipherSuiteLabel.values().length + " " + SHA256_OF_EMPTY.length()
                + " " + fastHash("x".getBytes()));
    }
}
