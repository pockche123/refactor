public class IntellijComponent11 {
    
    private void processInternal() {
        System.out.println("Internal processing");
    }
    
    public void processFile() {
        processInternal();
        System.out.println("File processed");
    }
    
    public String getComponentInfo() {
        return "IntelliJ IDE component";
    }
}