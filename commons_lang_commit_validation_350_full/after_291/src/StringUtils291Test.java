public class StringUtils291Test {
    
    public static void main(String[] args) {
        StringUtils291 utils = new StringUtils291();
        StringHelper291 helper = new StringHelper291();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils291.isEmpty("");
        String capitalized = StringUtils291.capitalize("hello");
        String reversed = StringHelper291.reverse("hello");
        String helperInfo = StringHelper291.getHelperInfo();
        
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