public class StringUtils328 {
    
    public static String padLeft(String str) {
        int targetLength = 10;
        if (str == null || str.length() >= targetLength) {
            return str;
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < targetLength - str.length(); i++) {
            sb.append(' ');
        }
        sb.append(str);
        return sb.toString();
    }
    
    public static String getUtilityInfo() {
        return "Commons Lang utility";
    }
}