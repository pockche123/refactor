public class StringUtils334Test {
    
    public static void main(String[] args) {
        StringUtils334 utils = new StringUtils334();
        StringHelper334 helper = new StringHelper334();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils334.isEmpty("");
        String capitalized = StringUtils334.capitalize("hello");
        String reversed = StringHelper334.reverse("hello");
        String helperInfo = StringHelper334.getHelperInfo();
        
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