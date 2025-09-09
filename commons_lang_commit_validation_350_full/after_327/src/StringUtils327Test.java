public class StringUtils327Test {
    
    public static void main(String[] args) {
        StringUtils327 utils = new StringUtils327();
        StringHelper327 helper = new StringHelper327();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils327.isEmpty("");
        String capitalized = StringUtils327.capitalize("hello");
        String reversed = StringHelper327.reverse("hello");
        String helperInfo = StringHelper327.getHelperInfo();
        
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