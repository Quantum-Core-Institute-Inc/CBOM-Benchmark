import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.HexFormat;

/** Tier 1: direct, literal MessageDigest lookups. */
public class T1Hashes {
    public static void main(String[] args) throws Exception {
        byte[] payload = "cbom-testbench".getBytes(StandardCharsets.UTF_8);

        byte[] legacy = MessageDigest.getInstance("MD5").digest(payload);
        byte[] gitStyle = MessageDigest.getInstance("SHA-1").digest(payload);
        byte[] content = MessageDigest.getInstance("SHA-256").digest(payload);
        byte[] sponge = MessageDigest.getInstance("SHA3-256").digest(payload);

        HexFormat hex = HexFormat.of();
        System.out.println(hex.formatHex(legacy) + " " + hex.formatHex(gitStyle) + " "
                + hex.formatHex(content) + " " + hex.formatHex(sponge));
    }
}
