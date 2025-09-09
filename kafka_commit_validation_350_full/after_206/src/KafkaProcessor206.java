public class KafkaProcessor206 {
    
    public void processMessage() {
        Long messageId = System.currentTimeMillis();
        System.out.println("Processing: " + messageId);
    }
    
    public String getStatus() {
        return "processing";
    }
}