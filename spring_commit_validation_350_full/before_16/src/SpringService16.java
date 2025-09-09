public class SpringService16 {
    
    public String processData() {
        return "result-" + System.currentTimeMillis();
    }
    
    public String getStatus() {
        return "active";
    }
}