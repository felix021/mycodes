import java.io.File;
import net.erdfelt.android.apk.AndroidApk;

public class VersionCode
{
    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.out.println("Usage: java VersionCode <apk_file>");
            System.exit(-1);
        }
        String filename = args[0];
        File apkFile = new File(filename);
        if (!apkFile.exists()) {
            System.exit(-1);
        }

        try {
            AndroidApk apk = new AndroidApk(apkFile);
            int code = Integer.parseInt(apk.getAppVersionCode());
            System.out.println(code);
        } catch (Throwable t) {
            t.printStackTrace(System.err);
            System.out.println("Error: unable to get version_code from apk_file");
        }
    }
}