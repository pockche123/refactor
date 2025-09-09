public class StringUtils235Test {
    
    public static void main(String[] args) {
        StringUtils235 utils = new StringUtils235();
        StringHelper235 helper = new StringHelper235();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils235.isEmpty("");
        String capitalized = StringUtils235.capitalize("hello");
        String reversed = StringHelper235.reverse("hello");
        String helperInfo = StringHelper235.getHelperInfo();
        
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