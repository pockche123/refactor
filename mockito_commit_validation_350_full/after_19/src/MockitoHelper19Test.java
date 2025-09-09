public class MockitoHelper19Test {
    
    public static void main(String[] args) {
        MockitoHelper19 helper = new MockitoHelper19();
        
        // Test functionality
        int count = helper.getMockCount();
        String testInfo = helper.getTestInfo();
        
        // Simple validation
        int testsRun = 2;
        int testsPassed = 0;
        
        if (testInfo != null && testInfo.contains("Mockito")) {
            testsPassed++;
        }
        
        if (count == 5) {
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