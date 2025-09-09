public class StringUtils107Test {
    
    public static void main(String[] args) {
        StringUtils107 utils = new StringUtils107();
        StringHelper107 helper = new StringHelper107();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils107.isEmpty("");
        String capitalized = StringUtils107.capitalize("hello");
        String reversed = StringHelper107.reverse("hello");
        String helperInfo = StringHelper107.getHelperInfo();
        
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