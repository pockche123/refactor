public class StringUtils10Test {
    
    public static void main(String[] args) {
        StringUtils10 utils = new StringUtils10();
        StringHelper10 helper = new StringHelper10();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils10.isEmpty("");
        String capitalized = StringUtils10.capitalize("hello");
        String reversed = StringHelper10.reverse("hello");
        String helperInfo = StringHelper10.getHelperInfo();
        
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