public class StringUtils16Test {
    
    public static void main(String[] args) {
        StringUtils16 utils = new StringUtils16();
        StringHelper16 helper = new StringHelper16();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils16.isEmpty("");
        String capitalized = StringUtils16.capitalize("hello");
        String reversed = StringHelper16.reverse("hello");
        String helperInfo = StringHelper16.getHelperInfo();
        
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