public class StringUtils116Test {
    
    public static void main(String[] args) {
        StringUtils116 utils = new StringUtils116();
        StringHelper116 helper = new StringHelper116();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils116.isEmpty("");
        String capitalized = StringUtils116.capitalize("hello");
        String reversed = StringHelper116.reverse("hello");
        String helperInfo = StringHelper116.getHelperInfo();
        
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