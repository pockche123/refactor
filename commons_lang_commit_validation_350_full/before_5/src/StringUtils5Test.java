public class StringUtils5Test {
    
    public static void main(String[] args) {
        StringUtils5 utils = new StringUtils5();
        StringHelper5 helper = new StringHelper5();
        
        // Test functionality
        boolean isEmpty = StringUtils5.isEmpty("");
        String capitalized = StringUtils5.capitalize("hello");
        String reversed = StringUtils5.reverse("hello");
        String helperInfo = StringHelper5.getHelperInfo();
        
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