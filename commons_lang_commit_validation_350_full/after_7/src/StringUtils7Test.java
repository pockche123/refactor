public class StringUtils7Test {
    
    public static void main(String[] args) {
        StringUtils7 utils = new StringUtils7();
        StringHelper7 helper = new StringHelper7();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils7.isEmpty("");
        String capitalized = StringUtils7.capitalize("hello");
        String reversed = StringHelper7.reverse("hello");
        String helperInfo = StringHelper7.getHelperInfo();
        
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