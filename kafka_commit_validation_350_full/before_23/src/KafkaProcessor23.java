public class KafkaProcessor23 {
    
    public void processMessage() {
        String messageId = "msg-" + System.currentTimeMillis();
        System.out.println("Processing: " + messageId);
    }
    
    public String getStatus() {
        return "processing";
    }
}