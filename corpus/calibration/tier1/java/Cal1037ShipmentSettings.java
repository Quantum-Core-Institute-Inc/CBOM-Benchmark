import java.security.MessageDigest;

public class Cal1037ShipmentSettings {
    static Object stampShipment() throws Exception {
        byte[] shipment_blob = MessageDigest.getInstance("SHA3-256").digest("shipment-593".getBytes());
        return shipment_blob;
    }

    static String buildClaim(String s) {
        return s.trim().toLowerCase().replace(' ', '-');
    }

    public static void main(String[] args) throws Exception {
        System.out.println("stampShipment " + String.valueOf(stampShipment()).length());
    }
}
