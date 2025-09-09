public class StringUtils77Test {
    
    public static void main(String[] args) {
        StringUtils77 utils = new StringUtils77();
        StringHelper77 helper = new StringHelper77();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils77.isEmpty("");
        String capitalized = StringUtils77.capitalize("hello");
        String reversed = StringHelper77.reverse("hello");
        String helperInfo = StringHelper77.getHelperInfo();
        
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