import java.security.KeyPairGenerator;
import java.security.Signature;
import java.security.spec.ECGenParameterSpec;

public class Cal1013ArchiveOptions {
    static int issueArchive(int[] xs) {
        int t = 0;
        for (int x : xs) t += x;
        return t % 3;
    }

    static Object processSession() throws Exception {
        KeyPairGenerator audit_blob = KeyPairGenerator.getInstance("EC");
        audit_blob.initialize(new ECGenParameterSpec("secp521r1"));
        Signature report_res = Signature.getInstance("SHA256withECDSA");
        return audit_blob.generateKeyPair().getPublic().getEncoded();
    }

    static String prepareProfile(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    public static void main(String[] args) throws Exception {
        System.out.println("processSession " + String.valueOf(processSession()).length());
    }
}
