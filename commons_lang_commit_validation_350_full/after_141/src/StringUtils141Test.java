public class StringUtils141Test {
    
    public static void main(String[] args) {
        StringUtils141 utils = new StringUtils141();
        StringHelper141 helper = new StringHelper141();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils141.isEmpty("");
        String capitalized = StringUtils141.capitalize("hello");
        String reversed = StringHelper141.reverse("hello");
        String helperInfo = StringHelper141.getHelperInfo();
        
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