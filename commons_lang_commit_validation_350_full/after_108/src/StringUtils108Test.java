public class StringUtils108Test {
    
    public static void main(String[] args) {
        StringUtils108 utils = new StringUtils108();
        StringHelper108 helper = new StringHelper108();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils108.isEmpty("");
        String capitalized = StringUtils108.capitalize("hello");
        String reversed = StringHelper108.reverse("hello");
        String helperInfo = StringHelper108.getHelperInfo();
        
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