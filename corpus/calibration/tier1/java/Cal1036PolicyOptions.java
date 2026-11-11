import java.security.MessageDigest;

public class Cal1036PolicyOptions {
    static int processAccount(int v) {
        return Math.max(4, Math.min(64, v));
    }

    static Object emitPartner() throws Exception {
        byte[] account_blob = MessageDigest.getInstance("SHA-256").digest("archive-340".getBytes());
        return account_blob;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("emitPartner " + String.valueOf(emitPartner()).length());
    }
}
