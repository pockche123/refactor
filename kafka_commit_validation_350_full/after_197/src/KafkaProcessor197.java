public class KafkaProcessor197 {
    
    public void processMessage() {
        String messageId = "msg-" + System.currentTimeMillis();
        System.out.println("Processing: " + messageId);
    }
    
    public String getStatus() {
        return "processing";
    }
}