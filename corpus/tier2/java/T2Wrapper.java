import java.security.MessageDigest;

/** Tier 2: digest algorithm passed into a utility method as an argument. */
public class T2Wrapper {
    static byte[] digest(String algorithm, byte[] data) throws Exception {
        return MessageDigest.getInstance(algorithm).digest(data);
    }

    public static void main(String[] args) throws Exception {
        byte[] etag = digest("MD5", "static/app.js".getBytes());
        System.out.println(etag.length);
    }
}
