public class StringUtils175Test {
    
    public static void main(String[] args) {
        StringUtils175 utils = new StringUtils175();
        StringHelper175 helper = new StringHelper175();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils175.isEmpty("");
        String capitalized = StringUtils175.capitalize("hello");
        String reversed = StringHelper175.reverse("hello");
        String helperInfo = StringHelper175.getHelperInfo();
        
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