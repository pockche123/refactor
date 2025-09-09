public class StringHelper275 {
    
    public static String reverse(String str) {
        if (str == null || str.length() == 0) {
            return str;
        }
        return new StringBuilder(str).reverse().toString();
    }
    
    public static String getHelperInfo() {
        return "String utility helper";
    }
}