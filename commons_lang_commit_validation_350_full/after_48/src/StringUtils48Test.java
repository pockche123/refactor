public class StringUtils48Test {
    
    public static void main(String[] args) {
        StringUtils48 utils = new StringUtils48();
        StringHelper48 helper = new StringHelper48();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils48.isEmpty("");
        String capitalized = StringUtils48.capitalize("hello");
        String reversed = StringHelper48.reverse("hello");
        String helperInfo = StringHelper48.getHelperInfo();
        
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