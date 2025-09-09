public class StringUtils84Test {
    
    public static void main(String[] args) {
        StringUtils84 utils = new StringUtils84();
        StringHelper84 helper = new StringHelper84();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils84.isEmpty("");
        String capitalized = StringUtils84.capitalize("hello");
        String reversed = StringHelper84.reverse("hello");
        String helperInfo = StringHelper84.getHelperInfo();
        
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