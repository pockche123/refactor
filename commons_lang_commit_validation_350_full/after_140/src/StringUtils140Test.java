public class StringUtils140Test {
    
    public static void main(String[] args) {
        StringUtils140 utils = new StringUtils140();
        StringHelper140 helper = new StringHelper140();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils140.isEmpty("");
        String capitalized = StringUtils140.capitalize("hello");
        String reversed = StringHelper140.reverse("hello");
        String helperInfo = StringHelper140.getHelperInfo();
        
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