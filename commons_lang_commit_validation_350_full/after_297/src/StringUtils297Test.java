public class StringUtils297Test {
    
    public static void main(String[] args) {
        StringUtils297 utils = new StringUtils297();
        StringHelper297 helper = new StringHelper297();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils297.isEmpty("");
        String capitalized = StringUtils297.capitalize("hello");
        String reversed = StringHelper297.reverse("hello");
        String helperInfo = StringHelper297.getHelperInfo();
        
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