public class StringUtils195Test {
    
    public static void main(String[] args) {
        StringUtils195 utils = new StringUtils195();
        StringHelper195 helper = new StringHelper195();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils195.isEmpty("");
        String capitalized = StringUtils195.capitalize("hello");
        String reversed = StringHelper195.reverse("hello");
        String helperInfo = StringHelper195.getHelperInfo();
        
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