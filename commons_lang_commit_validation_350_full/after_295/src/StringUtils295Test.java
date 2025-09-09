public class StringUtils295Test {
    
    public static void main(String[] args) {
        StringUtils295 utils = new StringUtils295();
        StringHelper295 helper = new StringHelper295();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils295.isEmpty("");
        String capitalized = StringUtils295.capitalize("hello");
        String reversed = StringHelper295.reverse("hello");
        String helperInfo = StringHelper295.getHelperInfo();
        
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