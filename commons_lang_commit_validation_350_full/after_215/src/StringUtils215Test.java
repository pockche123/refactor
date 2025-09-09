public class StringUtils215Test {
    
    public static void main(String[] args) {
        StringUtils215 utils = new StringUtils215();
        StringHelper215 helper = new StringHelper215();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils215.isEmpty("");
        String capitalized = StringUtils215.capitalize("hello");
        String reversed = StringHelper215.reverse("hello");
        String helperInfo = StringHelper215.getHelperInfo();
        
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