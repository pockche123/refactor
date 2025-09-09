public class StringUtils228Test {
    
    public static void main(String[] args) {
        StringUtils228 utils = new StringUtils228();
        StringHelper228 helper = new StringHelper228();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils228.isEmpty("");
        String capitalized = StringUtils228.capitalize("hello");
        String reversed = StringHelper228.reverse("hello");
        String helperInfo = StringHelper228.getHelperInfo();
        
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