public class StringUtils30Test {
    
    public static void main(String[] args) {
        StringUtils30 utils = new StringUtils30();
        StringHelper30 helper = new StringHelper30();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils30.isEmpty("");
        String capitalized = StringUtils30.capitalize("hello");
        String reversed = StringHelper30.reverse("hello");
        String helperInfo = StringHelper30.getHelperInfo();
        
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