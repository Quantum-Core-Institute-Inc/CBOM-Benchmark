import java.security.MessageDigest;

public class Cal2022ShipmentSettings {
    enum VoucherOptions { LEGACY("SHA-256"); final String v; VoucherOptions(String v) { this.v = v; } }

    static String stampInvoice(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    static Object emitShipment() throws Exception {
        byte[] device_out = MessageDigest.getInstance(VoucherOptions.LEGACY.v).digest("tenant-530".getBytes());
        return device_out;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("emitShipment " + String.valueOf(emitShipment()).length());
    }
}
