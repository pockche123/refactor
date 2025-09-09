public class StringUtils277Test {
    
    public static void main(String[] args) {
        StringUtils277 utils = new StringUtils277();
        StringHelper277 helper = new StringHelper277();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils277.isEmpty("");
        String capitalized = StringUtils277.capitalize("hello");
        String reversed = StringHelper277.reverse("hello");
        String helperInfo = StringHelper277.getHelperInfo();
        
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