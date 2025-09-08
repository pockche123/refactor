public class CompletionPhase {
    
    public void processMethod(/* @NotNull */ String editor) {
        System.out.println("Processing: " + editor);
    }
    
    public String getStatus() {
        return "working";
    }
}