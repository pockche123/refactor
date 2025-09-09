public class IntellijComponent141Test {
    
    public static void main(String[] args) {
        IntellijComponent141 component = new IntellijComponent141();
        
        // Test functionality
        component.processFile();
        String componentInfo = component.getComponentInfo();
        
        // Simple validation
        int testsRun = 2;
        int testsPassed = 0;
        
        if (componentInfo != null && componentInfo.contains("IntelliJ")) {
            testsPassed++;
        }
        
        try {
            component.processFile();
            testsPassed++;
        } catch (Exception e) {
            // Test failed
        }
        
        System.out.println("Tests run: " + testsRun);
        System.out.println("Tests passed: " + testsPassed);
        System.out.println("Tests failed: " + (testsRun - testsPassed));
        
        if (testsPassed == testsRun) {
            System.out.println("ALL TESTS PASSED!");
        } else {
            System.out.println("SOME TESTS FAILED!");
        }
    }
}