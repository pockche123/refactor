public class StringUtils257Test {
    
    public static void main(String[] args) {
        StringUtils257 utils = new StringUtils257();
        StringHelper257 helper = new StringHelper257();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils257.isEmpty("");
        String capitalized = StringUtils257.capitalize("hello");
        String reversed = StringHelper257.reverse("hello");
        String helperInfo = StringHelper257.getHelperInfo();
        
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