public class StringUtils80Test {
    
    public static void main(String[] args) {
        // Test functionality
        boolean isEmpty = StringUtils80.isEmpty("");
        String utilityInfo = StringUtils80.getUtilityInfo();
        
        // Simple validation
        int testsRun = 2;
        int testsPassed = 0;
        
        if (isEmpty) {
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