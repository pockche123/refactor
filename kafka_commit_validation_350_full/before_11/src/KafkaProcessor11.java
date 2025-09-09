public class KafkaProcessor11 {
    
    public void processMessage(String topic) {
        System.out.println("Processing message from topic: " + topic);
    }
    
    public String getStatus() {
        return "processing";
    }
}