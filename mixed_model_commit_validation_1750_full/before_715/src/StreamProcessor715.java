public class StreamProcessor715 {
    
    public void processData(String context) {
        System.out.println("Processing kafka data with context: " + (context != null ? context : "default"));
    }
    
    public String getDomainInfo() {
        return "kafka domain component";
    }
}