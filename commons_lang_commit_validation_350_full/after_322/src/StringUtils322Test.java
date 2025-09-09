public class StringUtils322Test {
    
    public static void main(String[] args) {
        StringUtils322 utils = new StringUtils322();
        StringHelper322 helper = new StringHelper322();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils322.isEmpty("");
        String capitalized = StringUtils322.capitalize("hello");
        String reversed = StringHelper322.reverse("hello");
        String helperInfo = StringHelper322.getHelperInfo();
        
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