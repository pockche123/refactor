public class StringUtils314Test {
    
    public static void main(String[] args) {
        StringUtils314 utils = new StringUtils314();
        StringHelper314 helper = new StringHelper314();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils314.isEmpty("");
        String capitalized = StringUtils314.capitalize("hello");
        String reversed = StringHelper314.reverse("hello");
        String helperInfo = StringHelper314.getHelperInfo();
        
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