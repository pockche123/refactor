public class StringUtils285Test {
    
    public static void main(String[] args) {
        StringUtils285 utils = new StringUtils285();
        StringHelper285 helper = new StringHelper285();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils285.isEmpty("");
        String capitalized = StringUtils285.capitalize("hello");
        String reversed = StringHelper285.reverse("hello");
        String helperInfo = StringHelper285.getHelperInfo();
        
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