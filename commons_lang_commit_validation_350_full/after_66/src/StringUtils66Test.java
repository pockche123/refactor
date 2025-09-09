public class StringUtils66Test {
    
    public static void main(String[] args) {
        StringUtils66 utils = new StringUtils66();
        StringHelper66 helper = new StringHelper66();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils66.isEmpty("");
        String capitalized = StringUtils66.capitalize("hello");
        String reversed = StringHelper66.reverse("hello");
        String helperInfo = StringHelper66.getHelperInfo();
        
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