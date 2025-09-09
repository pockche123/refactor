public class StringUtils23Test {
    
    public static void main(String[] args) {
        StringUtils23 utils = new StringUtils23();
        StringHelper23 helper = new StringHelper23();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils23.isEmpty("");
        String capitalized = StringUtils23.capitalize("hello");
        String reversed = StringHelper23.reverse("hello");
        String helperInfo = StringHelper23.getHelperInfo();
        
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