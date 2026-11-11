import java.security.MessageDigest;

/** Tier 2: algorithm names held in an enum; either constant is reachable at runtime. */
public class T2Enum {
    enum HashPolicy {
        LEGACY("SHA-1"),
        CURRENT("SHA-256");

        final String jcaName;

        HashPolicy(String jcaName) {
            this.jcaName = jcaName;
        }
    }

    public static void main(String[] args) throws Exception {
        HashPolicy policy = args.length > 0 ? HashPolicy.valueOf(args[0]) : HashPolicy.LEGACY;
        byte[] d = MessageDigest.getInstance(policy.jcaName).digest("ledger-entry".getBytes());
        System.out.println(policy + " " + d.length);
    }
}
