public class KafkaProcessor218 {
    
    public void processMessage() {
        String msgId = "msg-" + System.currentTimeMillis();
        System.out.println("Processing: " + msgId);
    }
    
    public String getStatus() {
        return "processing";
    }
}