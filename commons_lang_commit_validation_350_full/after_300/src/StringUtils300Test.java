public class StringUtils300Test {
    
    public static void main(String[] args) {
        StringUtils300 utils = new StringUtils300();
        StringHelper300 helper = new StringHelper300();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils300.isEmpty("");
        String capitalized = StringUtils300.capitalize("hello");
        String reversed = StringHelper300.reverse("hello");
        String helperInfo = StringHelper300.getHelperInfo();
        
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