import com.acme.vault.TokenVault;

/** Entry point; the only name ProGuard keeps. */
public class Main {
    public static void main(String[] args) throws Exception {
        System.out.println(TokenVault.selfTest());
    }
}
