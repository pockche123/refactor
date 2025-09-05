public class CompletionProgressIndicator {
    
    public void processMethod(/* @NotNull */ String parameters) {
        System.out.println("Processing: " + parameters);
    }
    
    public String getStatus() {
        return "working";
    }
}