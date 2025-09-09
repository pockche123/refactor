public class StringUtils62Test {
    
    public static void main(String[] args) {
        StringUtils62 utils = new StringUtils62();
        StringHelper62 helper = new StringHelper62();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils62.isEmpty("");
        String capitalized = StringUtils62.capitalize("hello");
        String reversed = StringHelper62.reverse("hello");
        String helperInfo = StringHelper62.getHelperInfo();
        
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