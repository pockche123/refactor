public class StringUtils124Test {
    
    public static void main(String[] args) {
        StringUtils124 utils = new StringUtils124();
        StringHelper124 helper = new StringHelper124();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils124.isEmpty("");
        String capitalized = StringUtils124.capitalize("hello");
        String reversed = StringHelper124.reverse("hello");
        String helperInfo = StringHelper124.getHelperInfo();
        
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