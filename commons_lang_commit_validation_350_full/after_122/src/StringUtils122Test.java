public class StringUtils122Test {
    
    public static void main(String[] args) {
        StringUtils122 utils = new StringUtils122();
        StringHelper122 helper = new StringHelper122();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils122.isEmpty("");
        String capitalized = StringUtils122.capitalize("hello");
        String reversed = StringHelper122.reverse("hello");
        String helperInfo = StringHelper122.getHelperInfo();
        
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