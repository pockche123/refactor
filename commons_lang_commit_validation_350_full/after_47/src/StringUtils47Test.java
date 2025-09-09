public class StringUtils47Test {
    
    public static void main(String[] args) {
        StringUtils47 utils = new StringUtils47();
        StringHelper47 helper = new StringHelper47();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils47.isEmpty("");
        String capitalized = StringUtils47.capitalize("hello");
        String reversed = StringHelper47.reverse("hello");
        String helperInfo = StringHelper47.getHelperInfo();
        
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