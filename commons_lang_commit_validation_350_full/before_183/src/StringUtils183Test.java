public class StringUtils183Test {
    
    public static void main(String[] args) {
        // Test functionality
        boolean result = StringUtils183.isBlank("  ");
        String utilityInfo = StringUtils183.getUtilityInfo();
        
        // Simple validation
        int testsRun = 2;
        int testsPassed = 0;
        
        if (result) {
            testsPassed++;
        }
        
        if (utilityInfo != null && utilityInfo.contains("Commons Lang")) {
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