public class KafkaProcessor {
    
    public void processMessage13() {
        String messageId = "msg-" + System.currentTimeMillis();
        System.out.println("Processing: " + messageId);
    }
    
    public String getStatus() {
        return "processing";
    }
}