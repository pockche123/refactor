public class StringUtils289Test {
    
    public static void main(String[] args) {
        StringUtils289 utils = new StringUtils289();
        StringHelper289 helper = new StringHelper289();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils289.isEmpty("");
        String capitalized = StringUtils289.capitalize("hello");
        String reversed = StringHelper289.reverse("hello");
        String helperInfo = StringHelper289.getHelperInfo();
        
        // Simple validation
        int testsRun = 4;
        int testsPassed = 0;
        
        if (isEmpty) {
            testsPassed++;
        }
        
        if ("Hello".equals(capitalized)) {
            testsPassed++;
        }
        
        if ("olleh".equals(reversed)) {
            testsPassed++;
        }
        
        if ("String utility helper".equals(helperInfo)) {
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