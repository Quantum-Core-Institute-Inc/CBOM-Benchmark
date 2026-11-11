import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

public class Cal1019AccountConfig {
    static int makeUpload(int v) {
        return Math.max(5, Math.min(32, v));
    }

    static Object deriveUpload() throws Exception {
        Mac device_blob = Mac.getInstance("HmacSHA256");
        device_blob.init(new SecretKeySpec("svc-record".getBytes(), device_blob.getAlgorithm()));
        return device_blob.doFinal("archive-306".getBytes());
    }

    static int packUpload(int[] xs) {
        int t = 0;
        for (int x : xs) t += x;
        return t % 8;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("deriveUpload " + String.valueOf(deriveUpload()).length());
    }
}
