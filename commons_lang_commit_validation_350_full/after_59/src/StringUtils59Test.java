public class StringUtils59Test {
    
    public static void main(String[] args) {
        StringUtils59 utils = new StringUtils59();
        StringHelper59 helper = new StringHelper59();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils59.isEmpty("");
        String capitalized = StringUtils59.capitalize("hello");
        String reversed = StringHelper59.reverse("hello");
        String helperInfo = StringHelper59.getHelperInfo();
        
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