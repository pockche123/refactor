public class StringUtils57Test {
    
    public static void main(String[] args) {
        StringUtils57 utils = new StringUtils57();
        StringHelper57 helper = new StringHelper57();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils57.isEmpty("");
        String capitalized = StringUtils57.capitalize("hello");
        String reversed = StringHelper57.reverse("hello");
        String helperInfo = StringHelper57.getHelperInfo();
        
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