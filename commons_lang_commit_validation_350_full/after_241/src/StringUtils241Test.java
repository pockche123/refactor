public class StringUtils241Test {
    
    public static void main(String[] args) {
        StringUtils241 utils = new StringUtils241();
        StringHelper241 helper = new StringHelper241();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils241.isEmpty("");
        String capitalized = StringUtils241.capitalize("hello");
        String reversed = StringHelper241.reverse("hello");
        String helperInfo = StringHelper241.getHelperInfo();
        
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