public class StringUtils329Test {
    
    public static void main(String[] args) {
        StringUtils329 utils = new StringUtils329();
        StringHelper329 helper = new StringHelper329();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils329.isEmpty("");
        String capitalized = StringUtils329.capitalize("hello");
        String reversed = StringHelper329.reverse("hello");
        String helperInfo = StringHelper329.getHelperInfo();
        
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