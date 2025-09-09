public class StringUtils276Test {
    
    public static void main(String[] args) {
        StringUtils276 utils = new StringUtils276();
        StringHelper276 helper = new StringHelper276();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils276.isEmpty("");
        String capitalized = StringUtils276.capitalize("hello");
        String reversed = StringHelper276.reverse("hello");
        String helperInfo = StringHelper276.getHelperInfo();
        
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