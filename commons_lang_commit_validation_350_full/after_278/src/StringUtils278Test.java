public class StringUtils278Test {
    
    public static void main(String[] args) {
        StringUtils278 utils = new StringUtils278();
        StringHelper278 helper = new StringHelper278();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils278.isEmpty("");
        String capitalized = StringUtils278.capitalize("hello");
        String reversed = StringHelper278.reverse("hello");
        String helperInfo = StringHelper278.getHelperInfo();
        
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