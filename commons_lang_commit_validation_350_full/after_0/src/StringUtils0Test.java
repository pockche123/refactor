public class StringUtils0Test {
    
    public static void main(String[] args) {
        StringUtils0 utils = new StringUtils0();
        StringHelper0 helper = new StringHelper0();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils0.isEmpty("");
        String capitalized = StringUtils0.capitalize("hello");
        String reversed = StringHelper0.reverse("hello");
        String helperInfo = StringHelper0.getHelperInfo();
        
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