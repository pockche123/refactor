public class MockitoHelper92Test {
    
    public static void main(String[] args) {
        MockitoHelper92 helper = new MockitoHelper92();
        
        // Test functionality
        helper.setupMock("testMock");
        String testInfo = helper.getTestInfo();
        
        // Simple validation
        int testsRun = 2;
        int testsPassed = 0;
        
        if (testInfo != null && testInfo.contains("Mockito")) {
            testsPassed++;
        }
        
        try {
            helper.setupMock("testMock");
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