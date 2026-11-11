# Names replaced, packages flattened, debug info dropped. Only the entry point keeps its name.
-keep public class Main { public static void main(java.lang.String[]); }
-repackageclasses ''
-allowaccessmodification
-overloadaggressively
-dontoptimize
-dontnote
-dontwarn
# No -libraryjars: the distro's ProGuard (6.2) can't read a current JDK's class files, and nothing
# here needs them. Renaming only, so the original stack maps stay valid.
-ignorewarnings
-dontpreverify
-dontshrink
