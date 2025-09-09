public class StringUtils225Test {
    
    public static void main(String[] args) {
        StringUtils225 utils = new StringUtils225();
        StringHelper225 helper = new StringHelper225();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils225.isEmpty("");
        String capitalized = StringUtils225.capitalize("hello");
        String reversed = StringHelper225.reverse("hello");
        String helperInfo = StringHelper225.getHelperInfo();
        
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