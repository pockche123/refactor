public class StringUtils167Test {
    
    public static void main(String[] args) {
        StringUtils167 utils = new StringUtils167();
        StringHelper167 helper = new StringHelper167();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils167.isEmpty("");
        String capitalized = StringUtils167.capitalize("hello");
        String reversed = StringHelper167.reverse("hello");
        String helperInfo = StringHelper167.getHelperInfo();
        
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