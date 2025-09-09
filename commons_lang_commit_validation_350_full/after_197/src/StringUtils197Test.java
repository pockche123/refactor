public class StringUtils197Test {
    
    public static void main(String[] args) {
        StringUtils197 utils = new StringUtils197();
        StringHelper197 helper = new StringHelper197();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils197.isEmpty("");
        String capitalized = StringUtils197.capitalize("hello");
        String reversed = StringHelper197.reverse("hello");
        String helperInfo = StringHelper197.getHelperInfo();
        
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