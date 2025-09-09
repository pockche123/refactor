public class SpringService200 {
    
    public String processData() {
        return String.valueOf(System.currentTimeMillis());
    }
    
    public String getStatus() {
        return "active";
    }
}