public class StringUtils246Test {
    
    public static void main(String[] args) {
        StringUtils246 utils = new StringUtils246();
        StringHelper246 helper = new StringHelper246();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils246.isEmpty("");
        String capitalized = StringUtils246.capitalize("hello");
        String reversed = StringHelper246.reverse("hello");
        String helperInfo = StringHelper246.getHelperInfo();
        
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