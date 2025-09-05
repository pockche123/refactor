public class CodeCompletionHandlerBase {
    
    public void processMethod(String initContext) {
        System.out.println("Processing: " + initContext);
    }
    
    public String getStatus() {
        return "working";
    }
}