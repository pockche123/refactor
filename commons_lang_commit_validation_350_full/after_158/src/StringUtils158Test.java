public class StringUtils158Test {
    
    public static void main(String[] args) {
        StringUtils158 utils = new StringUtils158();
        StringHelper158 helper = new StringHelper158();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils158.isEmpty("");
        String capitalized = StringUtils158.capitalize("hello");
        String reversed = StringHelper158.reverse("hello");
        String helperInfo = StringHelper158.getHelperInfo();
        
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