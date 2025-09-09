public class StringUtils145Test {
    
    public static void main(String[] args) {
        StringUtils145 utils = new StringUtils145();
        StringHelper145 helper = new StringHelper145();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils145.isEmpty("");
        String capitalized = StringUtils145.capitalize("hello");
        String reversed = StringHelper145.reverse("hello");
        String helperInfo = StringHelper145.getHelperInfo();
        
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