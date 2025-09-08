public class CompletionProgressIndicator {
    
    public void processMethod(String editor) {
        System.out.println("Processing: " + editor);
    }
    
    public String getStatus() {
        return "working";
    }
}