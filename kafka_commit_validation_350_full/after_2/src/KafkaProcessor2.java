public class KafkaProcessor2 {
    
    public void processMessage(String topic) {
        System.out.println("Processing message from topic: " + (topic != null ? topic : "default"));
    }
    
    public void processMessage() {
        processMessage("default");
    }
    
    public String getStatus() {
        return "processing";
    }
}