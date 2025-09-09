public class StringUtils83Test {
    
    public static void main(String[] args) {
        StringUtils83 utils = new StringUtils83();
        StringHelper83 helper = new StringHelper83();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils83.isEmpty("");
        String capitalized = StringUtils83.capitalize("hello");
        String reversed = StringHelper83.reverse("hello");
        String helperInfo = StringHelper83.getHelperInfo();
        
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