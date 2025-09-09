public class StringUtils254Test {
    
    public static void main(String[] args) {
        StringUtils254 utils = new StringUtils254();
        StringHelper254 helper = new StringHelper254();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils254.isEmpty("");
        String capitalized = StringUtils254.capitalize("hello");
        String reversed = StringHelper254.reverse("hello");
        String helperInfo = StringHelper254.getHelperInfo();
        
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