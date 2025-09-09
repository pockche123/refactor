public class StringUtils125Test {
    
    public static void main(String[] args) {
        StringUtils125 utils = new StringUtils125();
        StringHelper125 helper = new StringHelper125();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils125.isEmpty("");
        String capitalized = StringUtils125.capitalize("hello");
        String reversed = StringHelper125.reverse("hello");
        String helperInfo = StringHelper125.getHelperInfo();
        
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