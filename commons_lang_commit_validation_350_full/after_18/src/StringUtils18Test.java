public class StringUtils18Test {
    
    public static void main(String[] args) {
        StringUtils18 utils = new StringUtils18();
        StringHelper18 helper = new StringHelper18();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils18.isEmpty("");
        String capitalized = StringUtils18.capitalize("hello");
        String reversed = StringHelper18.reverse("hello");
        String helperInfo = StringHelper18.getHelperInfo();
        
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