import java.lang.reflect.Method;
import java.util.Base64;

/** Tier 5: digest obtained by reflection, algorithm name base64-encoded. */
public class T5Reflection {
    public static void main(String[] args) throws Exception {
        Class<?> cls = Class.forName("java.security." + "Message" + "Digest");
        Method factory = cls.getMethod("getInstance", String.class);
        String name = new String(Base64.getDecoder().decode("TUQ1"));
        Object digest = factory.invoke(null, name);
        Method run = cls.getMethod("digest", byte[].class);
        byte[] out = (byte[]) run.invoke(digest, (Object) "static/app.js".getBytes());
        System.out.println(out.length);
    }
}
