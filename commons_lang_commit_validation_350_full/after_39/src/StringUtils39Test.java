public class StringUtils39Test {
    
    public static void main(String[] args) {
        StringUtils39 utils = new StringUtils39();
        StringHelper39 helper = new StringHelper39();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils39.isEmpty("");
        String capitalized = StringUtils39.capitalize("hello");
        String reversed = StringHelper39.reverse("hello");
        String helperInfo = StringHelper39.getHelperInfo();
        
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