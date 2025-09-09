public class StringUtils269Test {
    
    public static void main(String[] args) {
        StringUtils269 utils = new StringUtils269();
        StringHelper269 helper = new StringHelper269();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils269.isEmpty("");
        String capitalized = StringUtils269.capitalize("hello");
        String reversed = StringHelper269.reverse("hello");
        String helperInfo = StringHelper269.getHelperInfo();
        
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