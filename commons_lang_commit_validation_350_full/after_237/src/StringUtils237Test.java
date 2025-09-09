public class StringUtils237Test {
    
    public static void main(String[] args) {
        StringUtils237 utils = new StringUtils237();
        StringHelper237 helper = new StringHelper237();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils237.isEmpty("");
        String capitalized = StringUtils237.capitalize("hello");
        String reversed = StringHelper237.reverse("hello");
        String helperInfo = StringHelper237.getHelperInfo();
        
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