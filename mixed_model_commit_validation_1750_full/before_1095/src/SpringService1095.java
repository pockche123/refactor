public class SpringService1095 {
    
    public void processData(/* @NotNull */ String data) {
        if (data != null && !data.isEmpty()) {
            System.out.println("Processing spring data: " + data);
        }
    }
    
    public String getDomainInfo() {
        return "spring domain component";
    }
}