public class StringUtils319Test {
    
    public static void main(String[] args) {
        StringUtils319 utils = new StringUtils319();
        StringHelper319 helper = new StringHelper319();
        
        // Test functionality
        boolean isEmpty = StringUtils319.isEmpty("");
        String capitalized = StringUtils319.capitalize("hello");
        String reversed = StringUtils319.reverse("hello");
        String helperInfo = StringHelper319.getHelperInfo();
        
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