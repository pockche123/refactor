public class StringUtils272Test {
    
    public static void main(String[] args) {
        StringUtils272 utils = new StringUtils272();
        StringHelper272 helper = new StringHelper272();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils272.isEmpty("");
        String capitalized = StringUtils272.capitalize("hello");
        String reversed = StringHelper272.reverse("hello");
        String helperInfo = StringHelper272.getHelperInfo();
        
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