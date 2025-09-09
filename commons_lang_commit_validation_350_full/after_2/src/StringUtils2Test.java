public class StringUtils2Test {
    
    public static void main(String[] args) {
        StringUtils2 utils = new StringUtils2();
        StringHelper2 helper = new StringHelper2();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils2.isEmpty("");
        String capitalized = StringUtils2.capitalize("hello");
        String reversed = StringHelper2.reverse("hello");
        String helperInfo = StringHelper2.getHelperInfo();
        
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