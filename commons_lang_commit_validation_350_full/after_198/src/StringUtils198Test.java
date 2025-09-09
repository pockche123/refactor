public class StringUtils198Test {
    
    public static void main(String[] args) {
        StringUtils198 utils = new StringUtils198();
        StringHelper198 helper = new StringHelper198();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils198.isEmpty("");
        String capitalized = StringUtils198.capitalize("hello");
        String reversed = StringHelper198.reverse("hello");
        String helperInfo = StringHelper198.getHelperInfo();
        
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