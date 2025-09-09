public class StringUtils287Test {
    
    public static void main(String[] args) {
        StringUtils287 utils = new StringUtils287();
        StringHelper287 helper = new StringHelper287();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils287.isEmpty("");
        String capitalized = StringUtils287.capitalize("hello");
        String reversed = StringHelper287.reverse("hello");
        String helperInfo = StringHelper287.getHelperInfo();
        
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