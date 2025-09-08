public class CompletionPhase {
    
    public void processMethod(/* @Nullable */ String indicator) {
        System.out.println("Processing: " + indicator);
    }
    
    public String getStatus() {
        return "working";
    }
}