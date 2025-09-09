public class StringUtils223Test {
    
    public static void main(String[] args) {
        StringUtils223 utils = new StringUtils223();
        StringHelper223 helper = new StringHelper223();
        
        // Test functionality
        boolean isEmpty = StringUtils223.isEmpty("");
        String capitalized = StringUtils223.capitalize("hello");
        String reversed = StringUtils223.reverse("hello");
        String helperInfo = StringHelper223.getHelperInfo();
        
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