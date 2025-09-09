public class StringUtils232Test {
    
    public static void main(String[] args) {
        StringUtils232 utils = new StringUtils232();
        StringHelper232 helper = new StringHelper232();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils232.isEmpty("");
        String capitalized = StringUtils232.capitalize("hello");
        String reversed = StringHelper232.reverse("hello");
        String helperInfo = StringHelper232.getHelperInfo();
        
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