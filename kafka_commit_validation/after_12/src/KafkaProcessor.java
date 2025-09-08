public class KafkaProcessor {
    
    public void processMessage12() {
        Long messageId = System.currentTimeMillis();
        System.out.println("Processing: " + messageId);
    }
    
    public String getStatus() {
        return "processing";
    }
}