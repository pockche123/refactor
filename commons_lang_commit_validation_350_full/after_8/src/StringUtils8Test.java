public class StringUtils8Test {
    
    public static void main(String[] args) {
        StringUtils8 utils = new StringUtils8();
        StringHelper8 helper = new StringHelper8();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils8.isEmpty("");
        String capitalized = StringUtils8.capitalize("hello");
        String reversed = StringHelper8.reverse("hello");
        String helperInfo = StringHelper8.getHelperInfo();
        
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