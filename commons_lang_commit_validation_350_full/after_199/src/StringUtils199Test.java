public class StringUtils199Test {
    
    public static void main(String[] args) {
        StringUtils199 utils = new StringUtils199();
        StringHelper199 helper = new StringHelper199();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils199.isEmpty("");
        String capitalized = StringUtils199.capitalize("hello");
        String reversed = StringHelper199.reverse("hello");
        String helperInfo = StringHelper199.getHelperInfo();
        
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