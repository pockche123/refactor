public class StringUtils129Test {
    
    public static void main(String[] args) {
        StringUtils129 utils = new StringUtils129();
        StringHelper129 helper = new StringHelper129();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils129.isEmpty("");
        String capitalized = StringUtils129.capitalize("hello");
        String reversed = StringHelper129.reverse("hello");
        String helperInfo = StringHelper129.getHelperInfo();
        
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