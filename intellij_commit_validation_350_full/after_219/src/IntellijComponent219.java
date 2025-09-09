public class IntellijComponent219 {
    
    public void processFile(/* @NotNull */ String filePath) {
        if (filePath != null && !filePath.isEmpty()) {
            System.out.println("Processing file: " + filePath);
        }
    }
    
    public String getComponentInfo() {
        return "IntelliJ IDE component";
    }
}