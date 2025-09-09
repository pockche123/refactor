public class StringUtils133Test {
    
    public static void main(String[] args) {
        StringUtils133 utils = new StringUtils133();
        StringHelper133 helper = new StringHelper133();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils133.isEmpty("");
        String capitalized = StringUtils133.capitalize("hello");
        String reversed = StringHelper133.reverse("hello");
        String helperInfo = StringHelper133.getHelperInfo();
        
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