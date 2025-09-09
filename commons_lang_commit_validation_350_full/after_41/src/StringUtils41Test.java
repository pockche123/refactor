public class StringUtils41Test {
    
    public static void main(String[] args) {
        StringUtils41 utils = new StringUtils41();
        StringHelper41 helper = new StringHelper41();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils41.isEmpty("");
        String capitalized = StringUtils41.capitalize("hello");
        String reversed = StringHelper41.reverse("hello");
        String helperInfo = StringHelper41.getHelperInfo();
        
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