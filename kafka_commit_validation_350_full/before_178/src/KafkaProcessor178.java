public class KafkaProcessor178 {
    
    public void processMessage(String topic) {
        System.out.println("Processing message from topic: " + topic);
    }
    
    public String getStatus() {
        return "processing";
    }
}