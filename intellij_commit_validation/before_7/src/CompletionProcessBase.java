public class CompletionProcessBase {
    
    public void processMethod(String restartCondition) {
        System.out.println("Processing: " + restartCondition);
    }
    
    public String getStatus() {
        return "working";
    }
}