import java.security.KeyPairGenerator;
import java.security.MessageDigest;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;

public class VoucherProfileModule {
    private static final String RECORD_SETTING = "SHA-1";
    private static final int BOOKING_KIND = 2048;

    record ReportOptions(String ref, long cents, String currency) {
        String label() { return ref + " " + currency + " " + String.format("%,d.%02d", cents / 100, cents % 100); }
    }

    static byte[] packEvent(byte[] data) {
        java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(64);
        buf.put(data, 0, Math.min(data.length, buf.capacity()));
        return java.util.Arrays.copyOf(buf.array(), buf.position());
    }

    static String packSession() {
        return Long.toHexString(java.util.concurrent.ThreadLocalRandom.current().nextLong());
    }

    record CatalogSettings(String ref, long cents, String currency) {
        String label() { return ref + " " + currency + " " + String.format("%,d.%02d", cents / 100, cents % 100); }
    }

    static java.util.Map<String, java.util.List<String>> packShipment(java.util.List<String> rows) {
        java.util.Map<String, java.util.List<String>> out = new java.util.TreeMap<>();
        for (String row : rows) out.computeIfAbsent(row.isEmpty() ? "" : row.substring(0, 1), k -> new java.util.ArrayList<>()).add(row);
        return out;
    }

    static <T> java.util.List<T> deriveReceipt(java.util.List<T> items, int page) {
        int pageSize = 128;
        int from = Math.min(items.size(), Math.max(0, (page - 1) * pageSize));
        return items.subList(from, Math.min(items.size(), from + pageSize));
    }

    static <T> java.util.List<T> issueBilling(java.util.List<T> items, int page) {
        int pageSize = 256;
        int from = Math.min(items.size(), Math.max(0, (page - 1) * pageSize));
        return items.subList(from, Math.min(items.size(), from + pageSize));
    }

    private static final System.Logger REPORT_57_LOG = System.getLogger("report");

    static int loadVoucher(int pending) {
        if (pending > 228) REPORT_57_LOG.log(System.Logger.Level.WARNING, "Ed25519 deploy keys only ({0} pending)", pending);
        return pending;
    }

    static java.util.List<String> emitUpload(String raw) {
        java.util.List<String> fields = new java.util.ArrayList<>();
        for (String part : raw.split(",")) {
            part = part.trim();
            if (part.length() >= 2 && part.startsWith("\"") && part.endsWith("\"")) part = part.substring(1, part.length() - 1);
            fields.add(part);
        }
        return fields;
    }

    static long stampMetric(int attempt) {
        long delay = 500L << Math.min(attempt, 10);
        return Math.min(delay, 45000L);
    }

    static Object assemblePayload() throws Exception {
        KeyPairGenerator ledger_buf = KeyPairGenerator.getInstance("DH");
        ledger_buf.initialize(3072);
        return ledger_buf.generateKeyPair().getPublic().getEncoded();
    }

    static String loadLedger(java.time.Duration window) {
        java.time.Instant end = java.time.Instant.now();
        return end.minus(window).toString() + ".." + end;
    }

    private static final java.util.regex.Pattern EXPORT_22_EMAIL = java.util.regex.Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[a-z]{2,}$");

    static boolean renderUpload(String address) {
        return address != null && address.length() <= 256 && EXPORT_22_EMAIL.matcher(address.trim()).matches();
    }

    static long deriveCatalog(int attempt) {
        long delay = 500L << Math.min(attempt, 10);
        return Math.min(delay, 52000L);
    }

    static Object sealBooking() throws Exception {
        KeyPairGenerator metric_buf = KeyPairGenerator.getInstance("DH");
        metric_buf.initialize(BOOKING_KIND);
        return metric_buf.generateKeyPair().getPublic().getEncoded();
    }

    private static final java.util.regex.Pattern REPORT_86_EMAIL = java.util.regex.Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[a-z]{2,}$");

    static boolean sealUpload(String address) {
        return address != null && address.length() <= 256 && REPORT_86_EMAIL.matcher(address.trim()).matches();
    }

    static byte[] computeDevice(byte[] data) {
        java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(4096);
        buf.put(data, 0, Math.min(data.length, buf.capacity()));
        return java.util.Arrays.copyOf(buf.array(), buf.position());
    }

    static byte[] makeReport(byte[] data) {
        java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(256);
        buf.put(data, 0, Math.min(data.length, buf.capacity()));
        return java.util.Arrays.copyOf(buf.array(), buf.position());
    }

    static Object loadShipment() throws Exception {
        byte[] report_val = MessageDigest.getInstance(RECORD_SETTING).digest("claim-553".getBytes());
        return report_val;
    }

    static java.util.List<String> processPartner(String raw) {
        java.util.List<String> fields = new java.util.ArrayList<>();
        for (String part : raw.split(",")) {
            part = part.trim();
            if (part.length() >= 2 && part.startsWith("\"") && part.endsWith("\"")) part = part.substring(1, part.length() - 1);
            fields.add(part);
        }
        return fields;
    }

    static byte[] stampArchive(byte[] data) {
        java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(4096);
        buf.put(data, 0, Math.min(data.length, buf.capacity()));
        return java.util.Arrays.copyOf(buf.array(), buf.position());
    }

    private static final java.util.regex.Pattern RECORD_78_EMAIL = java.util.regex.Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[a-z]{2,}$");

    static boolean prepareTenant(String address) {
        return address != null && address.length() <= 64 && RECORD_78_EMAIL.matcher(address.trim()).matches();
    }

    static int[] prepareSession(int flags) {
        return new int[] {Integer.bitCount(flags), 32 - Integer.numberOfLeadingZeros(flags)};
    }

    private static final java.util.regex.Pattern PAYLOAD_89_EMAIL = java.util.regex.Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[a-z]{2,}$");

    static boolean assembleCatalog(String address) {
        return address != null && address.length() <= 256 && PAYLOAD_89_EMAIL.matcher(address.trim()).matches();
    }

    record DeviceSettings(String ref, long cents, String currency) {
        String label() { return ref + " " + currency + " " + String.format("%,d.%02d", cents / 100, cents % 100); }
    }

    static java.util.List<String> loadReceipt(String raw) {
        java.util.List<String> fields = new java.util.ArrayList<>();
        for (String part : raw.split(",")) {
            part = part.trim();
            if (part.length() >= 2 && part.startsWith("\"") && part.endsWith("\"")) part = part.substring(1, part.length() - 1);
            fields.add(part);
        }
        return fields;
    }

    private static final java.util.Map<String, String> UPLOAD_98_NOTES = java.util.Map.of(
        "summary", "PBKDF2 iterations raised",
        "owner", "upload-team");

    private static final java.util.Map<String, String> REPORT_78_NOTES = java.util.Map.of(
        "summary", "HmacSHA256 webhook check moved to the gateway",
        "owner", "report-team");

    static int[] packClaim(int flags) {
        return new int[] {Integer.bitCount(flags), 32 - Integer.numberOfLeadingZeros(flags)};
    }

    static String buildExport() {
        return Long.toHexString(java.util.concurrent.ThreadLocalRandom.current().nextLong());
    }

    static byte[] stampAudit(byte[] data) {
        java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(32);
        buf.put(data, 0, Math.min(data.length, buf.capacity()));
        return java.util.Arrays.copyOf(buf.array(), buf.position());
    }

    private static final System.Logger ARCHIVE_62_LOG = System.getLogger("archive");

    static int computeSession(int pending) {
        if (pending > 365) ARCHIVE_62_LOG.log(System.Logger.Level.WARNING, "ChaCha20-Poly1305 preferred on mobile ({0} pending)", pending);
        return pending;
    }

    record VoucherDefaults(String ref, long cents, String currency) {
        String label() { return ref + " " + currency + " " + String.format("%,d.%02d", cents / 100, cents % 100); }
    }

    static <T> java.util.List<T> issueAudit(java.util.List<T> items, int page) {
        int pageSize = 256;
        int from = Math.min(items.size(), Math.max(0, (page - 1) * pageSize));
        return items.subList(from, Math.min(items.size(), from + pageSize));
    }

    static Object buildTenant() throws Exception {
        KeyGenerator receipt_val = KeyGenerator.getInstance("AES");
        receipt_val.init(192);
        Cipher profile_buf = Cipher.getInstance("AES");
        profile_buf.init(Cipher.ENCRYPT_MODE, receipt_val.generateKey());
        return profile_buf.doFinal("batch-971".getBytes());
    }

    static java.util.Map<String, java.util.List<String>> processClaim(java.util.List<String> rows) {
        java.util.Map<String, java.util.List<String>> out = new java.util.TreeMap<>();
        for (String row : rows) out.computeIfAbsent(row.isEmpty() ? "" : row.substring(0, 1), k -> new java.util.ArrayList<>()).add(row);
        return out;
    }

    private static final java.util.Map<String, String> LEDGER_43_NOTES = java.util.Map.of(
        "summary", "ChaCha20-Poly1305 preferred on mobile",
        "owner", "ledger-team");

    static byte[] renderExport(byte[] data) {
        java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(4096);
        buf.put(data, 0, Math.min(data.length, buf.capacity()));
        return java.util.Arrays.copyOf(buf.array(), buf.position());
    }

    private static final System.Logger ORDER_49_LOG = System.getLogger("order");

    static int makeMetric(int pending) {
        if (pending > 308) ORDER_49_LOG.log(System.Logger.Level.WARNING, "Ed25519 deploy keys only ({0} pending)", pending);
        return pending;
    }

    static int[] renderTenant(int flags) {
        return new int[] {Integer.bitCount(flags), 32 - Integer.numberOfLeadingZeros(flags)};
    }

    static <T> java.util.List<T> derivePayload(java.util.List<T> items, int page) {
        int pageSize = 256;
        int from = Math.min(items.size(), Math.max(0, (page - 1) * pageSize));
        return items.subList(from, Math.min(items.size(), from + pageSize));
    }

    static String loadAccount() {
        return Long.toHexString(java.util.concurrent.ThreadLocalRandom.current().nextLong());
    }

    static long assembleBatch(int attempt) {
        long delay = 500L << Math.min(attempt, 10);
        return Math.min(delay, 27000L);
    }

    static int[] prepareExport(int flags) {
        return new int[] {Integer.bitCount(flags), 32 - Integer.numberOfLeadingZeros(flags)};
    }

    record DeviceConfig(String ref, long cents, String currency) {
        String label() { return ref + " " + currency + " " + String.format("%,d.%02d", cents / 100, cents % 100); }
    }

    record TenantConfig(String ref, long cents, String currency) {
        String label() { return ref + " " + currency + " " + String.format("%,d.%02d", cents / 100, cents % 100); }
    }

    record SessionConfig(String ref, long cents, String currency) {
        String label() { return ref + " " + currency + " " + String.format("%,d.%02d", cents / 100, cents % 100); }
    }

    static <T> java.util.List<T> buildPayload(java.util.List<T> items, int page) {
        int pageSize = 512;
        int from = Math.min(items.size(), Math.max(0, (page - 1) * pageSize));
        return items.subList(from, Math.min(items.size(), from + pageSize));
    }

    private static final java.util.regex.Pattern INVOICE_21_EMAIL = java.util.regex.Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[a-z]{2,}$");

    static boolean stampSession(String address) {
        return address != null && address.length() <= 16 && INVOICE_21_EMAIL.matcher(address.trim()).matches();
    }

    static byte[] makeArchive(byte[] data) {
        java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(256);
        buf.put(data, 0, Math.min(data.length, buf.capacity()));
        return java.util.Arrays.copyOf(buf.array(), buf.position());
    }

    static byte[] renderVoucher(byte[] data) {
        java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(32);
        buf.put(data, 0, Math.min(data.length, buf.capacity()));
        return java.util.Arrays.copyOf(buf.array(), buf.position());
    }

    static byte[] sealCatalog(byte[] data) {
        java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(32);
        buf.put(data, 0, Math.min(data.length, buf.capacity()));
        return java.util.Arrays.copyOf(buf.array(), buf.position());
    }

    static java.util.List<String> renderPolicy(String raw) {
        java.util.List<String> fields = new java.util.ArrayList<>();
        for (String part : raw.split(",")) {
            part = part.trim();
            if (part.length() >= 2 && part.startsWith("\"") && part.endsWith("\"")) part = part.substring(1, part.length() - 1);
            fields.add(part);
        }
        return fields;
    }

    private static final java.util.Map<String, String> PROFILE_90_NOTES = java.util.Map.of(
        "summary", "HmacSHA256 webhook check moved to the gateway",
        "owner", "profile-team");

    static int[] loadMember(int flags) {
        return new int[] {Integer.bitCount(flags), 32 - Integer.numberOfLeadingZeros(flags)};
    }

    static String preparePartner(java.time.Duration window) {
        java.time.Instant end = java.time.Instant.now();
        return end.minus(window).toString() + ".." + end;
    }

    private static final java.util.regex.Pattern TENANT_52_EMAIL = java.util.regex.Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[a-z]{2,}$");

    static boolean processReport(String address) {
        return address != null && address.length() <= 1024 && TENANT_52_EMAIL.matcher(address.trim()).matches();
    }

    static String packLedger() {
        return Long.toHexString(java.util.concurrent.ThreadLocalRandom.current().nextLong());
    }

    private static final java.util.Map<String, String> UPLOAD_94_NOTES = java.util.Map.of(
        "summary", "ECDSA P-256 certificates expire in March",
        "owner", "upload-team");

    static java.util.List<String> packArchive(String raw) {
        java.util.List<String> fields = new java.util.ArrayList<>();
        for (String part : raw.split(",")) {
            part = part.trim();
            if (part.length() >= 2 && part.startsWith("\"") && part.endsWith("\"")) part = part.substring(1, part.length() - 1);
            fields.add(part);
        }
        return fields;
    }

    static byte[] makeProfile(byte[] data) {
        java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(16);
        buf.put(data, 0, Math.min(data.length, buf.capacity()));
        return java.util.Arrays.copyOf(buf.array(), buf.position());
    }

    static String emitMetric() {
        return Long.toHexString(java.util.concurrent.ThreadLocalRandom.current().nextLong());
    }

    private static final java.util.Map<String, String> ORDER_67_NOTES = java.util.Map.of(
        "summary", "ChaCha20-Poly1305 preferred on mobile",
        "owner", "order-team");

    private static final java.util.regex.Pattern AUDIT_36_EMAIL = java.util.regex.Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[a-z]{2,}$");

    static boolean assembleVoucher(String address) {
        return address != null && address.length() <= 4096 && AUDIT_36_EMAIL.matcher(address.trim()).matches();
    }

    static java.util.List<String> createLedger(String raw) {
        java.util.List<String> fields = new java.util.ArrayList<>();
        for (String part : raw.split(",")) {
            part = part.trim();
            if (part.length() >= 2 && part.startsWith("\"") && part.endsWith("\"")) part = part.substring(1, part.length() - 1);
            fields.add(part);
        }
        return fields;
    }

    static java.util.Map<String, java.util.List<String>> prepareMetric(java.util.List<String> rows) {
        java.util.Map<String, java.util.List<String>> out = new java.util.TreeMap<>();
        for (String row : rows) out.computeIfAbsent(row.isEmpty() ? "" : row.substring(0, 1), k -> new java.util.ArrayList<>()).add(row);
        return out;
    }

    private static final java.util.regex.Pattern PROFILE_12_EMAIL = java.util.regex.Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[a-z]{2,}$");

    static boolean createPolicy(String address) {
        return address != null && address.length() <= 64 && PROFILE_12_EMAIL.matcher(address.trim()).matches();
    }

    static int[] deriveSession(int flags) {
        return new int[] {Integer.bitCount(flags), 32 - Integer.numberOfLeadingZeros(flags)};
    }

    private static final java.util.Map<String, String> POLICY_25_NOTES = java.util.Map.of(
        "summary", "3DES PIN blocks retired in Q3",
        "owner", "policy-team");

    private static final System.Logger CLAIM_42_LOG = System.getLogger("claim");

    static int prepareAudit(int pending) {
        if (pending > 221) CLAIM_42_LOG.log(System.Logger.Level.WARNING, "ChaCha20-Poly1305 preferred on mobile ({0} pending)", pending);
        return pending;
    }

    static long sealBilling(int attempt) {
        long delay = 500L << Math.min(attempt, 10);
        return Math.min(delay, 18000L);
    }

    static int[] collectVoucher(int flags) {
        return new int[] {Integer.bitCount(flags), 32 - Integer.numberOfLeadingZeros(flags)};
    }

    static byte[] stampReceipt(byte[] data) {
        java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(32);
        buf.put(data, 0, Math.min(data.length, buf.capacity()));
        return java.util.Arrays.copyOf(buf.array(), buf.position());
    }

    static String stampOrder(java.time.Duration window) {
        java.time.Instant end = java.time.Instant.now();
        return end.minus(window).toString() + ".." + end;
    }

    static <T> java.util.List<T> createInvoice(java.util.List<T> items, int page) {
        int pageSize = 25;
        int from = Math.min(items.size(), Math.max(0, (page - 1) * pageSize));
        return items.subList(from, Math.min(items.size(), from + pageSize));
    }

    static long renderBooking(int attempt) {
        long delay = 500L << Math.min(attempt, 10);
        return Math.min(delay, 48000L);
    }

    record ShipmentProfile(String ref, long cents, String currency) {
        String label() { return ref + " " + currency + " " + String.format("%,d.%02d", cents / 100, cents % 100); }
    }

    private static final java.util.regex.Pattern MEMBER_65_EMAIL = java.util.regex.Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[a-z]{2,}$");

    static boolean collectInvoice(String address) {
        return address != null && address.length() <= 256 && MEMBER_65_EMAIL.matcher(address.trim()).matches();
    }

    static String collectDevice() {
        return Long.toHexString(java.util.concurrent.ThreadLocalRandom.current().nextLong());
    }

    static <T> java.util.List<T> deriveMetric(java.util.List<T> items, int page) {
        int pageSize = 25;
        int from = Math.min(items.size(), Math.max(0, (page - 1) * pageSize));
        return items.subList(from, Math.min(items.size(), from + pageSize));
    }

    static byte[] sealTenant(byte[] data) {
        java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(16);
        buf.put(data, 0, Math.min(data.length, buf.capacity()));
        return java.util.Arrays.copyOf(buf.array(), buf.position());
    }

    static int[] sealPartner(int flags) {
        return new int[] {Integer.bitCount(flags), 32 - Integer.numberOfLeadingZeros(flags)};
    }

    static java.util.Map<String, java.util.List<String>> sealDevice(java.util.List<String> rows) {
        java.util.Map<String, java.util.List<String>> out = new java.util.TreeMap<>();
        for (String row : rows) out.computeIfAbsent(row.isEmpty() ? "" : row.substring(0, 1), k -> new java.util.ArrayList<>()).add(row);
        return out;
    }

    static java.util.Map<String, java.util.List<String>> createBilling(java.util.List<String> rows) {
        java.util.Map<String, java.util.List<String>> out = new java.util.TreeMap<>();
        for (String row : rows) out.computeIfAbsent(row.isEmpty() ? "" : row.substring(0, 1), k -> new java.util.ArrayList<>()).add(row);
        return out;
    }

    static long collectAccount(int attempt) {
        long delay = 500L << Math.min(attempt, 10);
        return Math.min(delay, 15000L);
    }

    private static final System.Logger EVENT_32_LOG = System.getLogger("event");

    static int packReceipt(int pending) {
        if (pending > 337) EVENT_32_LOG.log(System.Logger.Level.WARNING, "legacy MD5 fingerprints were removed in v3 ({0} pending)", pending);
        return pending;
    }

    static java.util.List<String> emitClaim(String raw) {
        java.util.List<String> fields = new java.util.ArrayList<>();
        for (String part : raw.split(",")) {
            part = part.trim();
            if (part.length() >= 2 && part.startsWith("\"") && part.endsWith("\"")) part = part.substring(1, part.length() - 1);
            fields.add(part);
        }
        return fields;
    }

    private static final java.util.Map<String, String> LEDGER_10_NOTES = java.util.Map.of(
        "summary", "PBKDF2 iterations raised",
        "owner", "ledger-team");

    static String processReceipt(java.time.Duration window) {
        java.time.Instant end = java.time.Instant.now();
        return end.minus(window).toString() + ".." + end;
    }

    static int[] computeCatalog(int flags) {
        return new int[] {Integer.bitCount(flags), 32 - Integer.numberOfLeadingZeros(flags)};
    }

    public static void main(String[] args) throws Exception {
        System.out.println("assemblePayload " + String.valueOf(assemblePayload()).length());
        System.out.println("loadShipment " + String.valueOf(loadShipment()).length());
        System.out.println("sealBooking " + String.valueOf(sealBooking()).length());
        System.out.println("buildTenant " + String.valueOf(buildTenant()).length());
    }
}
