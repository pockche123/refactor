public class StringUtils13Test {
    
    public static void main(String[] args) {
        StringUtils13 utils = new StringUtils13();
        StringHelper13 helper = new StringHelper13();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils13.isEmpty("");
        String capitalized = StringUtils13.capitalize("hello");
        String reversed = StringHelper13.reverse("hello");
        String helperInfo = StringHelper13.getHelperInfo();
        
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