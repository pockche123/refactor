public class StringUtils190Test {
    
    public static void main(String[] args) {
        StringUtils190 utils = new StringUtils190();
        StringHelper190 helper = new StringHelper190();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils190.isEmpty("");
        String capitalized = StringUtils190.capitalize("hello");
        String reversed = StringHelper190.reverse("hello");
        String helperInfo = StringHelper190.getHelperInfo();
        
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