public class StringUtils136Test {
    
    public static void main(String[] args) {
        StringUtils136 utils = new StringUtils136();
        StringHelper136 helper = new StringHelper136();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils136.isEmpty("");
        String capitalized = StringUtils136.capitalize("hello");
        String reversed = StringHelper136.reverse("hello");
        String helperInfo = StringHelper136.getHelperInfo();
        
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