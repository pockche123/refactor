public class StringUtils271Test {
    
    public static void main(String[] args) {
        StringUtils271 utils = new StringUtils271();
        StringHelper271 helper = new StringHelper271();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils271.isEmpty("");
        String capitalized = StringUtils271.capitalize("hello");
        String reversed = StringHelper271.reverse("hello");
        String helperInfo = StringHelper271.getHelperInfo();
        
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