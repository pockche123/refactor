public class KafkaProcessor {
    
    public void processMessage16() {
        Long messageId = System.currentTimeMillis();
        System.out.println("Processing: " + messageId);
    }
    
    public String getStatus() {
        return "processing";
    }
}