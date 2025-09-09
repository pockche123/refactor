public class StringUtils139Test {
    
    public static void main(String[] args) {
        StringUtils139 utils = new StringUtils139();
        StringHelper139 helper = new StringHelper139();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils139.isEmpty("");
        String capitalized = StringUtils139.capitalize("hello");
        String reversed = StringHelper139.reverse("hello");
        String helperInfo = StringHelper139.getHelperInfo();
        
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