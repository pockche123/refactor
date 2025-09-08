public class KafkaProcessor {
    
    public String getMessageId17() {
        return "msg-" + System.currentTimeMillis();
    }
    
    public String getStatus() {
        return "processing";
    }
}