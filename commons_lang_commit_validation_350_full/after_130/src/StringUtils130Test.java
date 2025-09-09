public class StringUtils130Test {
    
    public static void main(String[] args) {
        StringUtils130 utils = new StringUtils130();
        StringHelper130 helper = new StringHelper130();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils130.isEmpty("");
        String capitalized = StringUtils130.capitalize("hello");
        String reversed = StringHelper130.reverse("hello");
        String helperInfo = StringHelper130.getHelperInfo();
        
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