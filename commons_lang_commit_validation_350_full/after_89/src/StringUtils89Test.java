public class StringUtils89Test {
    
    public static void main(String[] args) {
        StringUtils89 utils = new StringUtils89();
        StringHelper89 helper = new StringHelper89();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils89.isEmpty("");
        String capitalized = StringUtils89.capitalize("hello");
        String reversed = StringHelper89.reverse("hello");
        String helperInfo = StringHelper89.getHelperInfo();
        
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