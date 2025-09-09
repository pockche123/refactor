public class StringUtils312Test {
    
    public static void main(String[] args) {
        StringUtils312 utils = new StringUtils312();
        StringHelper312 helper = new StringHelper312();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils312.isEmpty("");
        String capitalized = StringUtils312.capitalize("hello");
        String reversed = StringHelper312.reverse("hello");
        String helperInfo = StringHelper312.getHelperInfo();
        
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