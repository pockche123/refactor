public class BaseCompletionLookupArranger {
    
    public void processMethod(/* @NotNull */ String runnable) {
        System.out.println("Processing: " + runnable);
    }
    
    public String getStatus() {
        return "working";
    }
}