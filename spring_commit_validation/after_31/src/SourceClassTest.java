public class SourceClassTest {
    
    public static void main(String[] args) {
        SourceClass obj = new SourceClass();
        
        // Test public method functionality
        String result = obj.processData();
        
        // Test status
        String status = obj.getStatus();
        
        // Simple test validation
        int testsRun = 2;
        int testsPassed = 0;
        
        if (status.equals("working")) {
            testsPassed++;
        }
        
        if ("helper result".equals(result)) {
            testsPassed++;
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