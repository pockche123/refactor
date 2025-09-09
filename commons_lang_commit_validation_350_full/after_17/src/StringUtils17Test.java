public class StringUtils17Test {
    
    public static void main(String[] args) {
        StringUtils17 utils = new StringUtils17();
        StringHelper17 helper = new StringHelper17();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils17.isEmpty("");
        String capitalized = StringUtils17.capitalize("hello");
        String reversed = StringHelper17.reverse("hello");
        String helperInfo = StringHelper17.getHelperInfo();
        
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