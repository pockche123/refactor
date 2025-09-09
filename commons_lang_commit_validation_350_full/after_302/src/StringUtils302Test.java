public class StringUtils302Test {
    
    public static void main(String[] args) {
        StringUtils302 utils = new StringUtils302();
        StringHelper302 helper = new StringHelper302();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils302.isEmpty("");
        String capitalized = StringUtils302.capitalize("hello");
        String reversed = StringHelper302.reverse("hello");
        String helperInfo = StringHelper302.getHelperInfo();
        
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