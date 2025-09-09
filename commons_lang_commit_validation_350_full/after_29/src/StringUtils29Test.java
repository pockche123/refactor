public class StringUtils29Test {
    
    public static void main(String[] args) {
        StringUtils29 utils = new StringUtils29();
        StringHelper29 helper = new StringHelper29();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils29.isEmpty("");
        String capitalized = StringUtils29.capitalize("hello");
        String reversed = StringHelper29.reverse("hello");
        String helperInfo = StringHelper29.getHelperInfo();
        
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