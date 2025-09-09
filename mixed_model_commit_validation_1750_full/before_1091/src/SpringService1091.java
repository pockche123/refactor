public class SpringService1091 {
    
    public void processData(String context) {
        System.out.println("Processing spring data with context: " + (context != null ? context : "default"));
    }
    
    public String getDomainInfo() {
        return "spring domain component";
    }
}