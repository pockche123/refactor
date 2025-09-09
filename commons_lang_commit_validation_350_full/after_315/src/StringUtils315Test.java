public class StringUtils315Test {
    
    public static void main(String[] args) {
        StringUtils315 utils = new StringUtils315();
        StringHelper315 helper = new StringHelper315();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils315.isEmpty("");
        String capitalized = StringUtils315.capitalize("hello");
        String reversed = StringHelper315.reverse("hello");
        String helperInfo = StringHelper315.getHelperInfo();
        
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