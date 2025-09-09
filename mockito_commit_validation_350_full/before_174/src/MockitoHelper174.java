public class MockitoHelper174 {
    
    public void setupMock(String mockName) {
        System.out.println("Setting up mock: " + (mockName != null ? mockName : "default"));
    }
    
    public String getTestInfo() {
        return "Mockito test helper";
    }
}