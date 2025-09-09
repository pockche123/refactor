public class StringUtils120Test {
    
    public static void main(String[] args) {
        StringUtils120 utils = new StringUtils120();
        StringHelper120 helper = new StringHelper120();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils120.isEmpty("");
        String capitalized = StringUtils120.capitalize("hello");
        String reversed = StringHelper120.reverse("hello");
        String helperInfo = StringHelper120.getHelperInfo();
        
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