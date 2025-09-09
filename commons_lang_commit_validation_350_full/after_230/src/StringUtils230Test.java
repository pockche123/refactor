public class StringUtils230Test {
    
    public static void main(String[] args) {
        StringUtils230 utils = new StringUtils230();
        StringHelper230 helper = new StringHelper230();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils230.isEmpty("");
        String capitalized = StringUtils230.capitalize("hello");
        String reversed = StringHelper230.reverse("hello");
        String helperInfo = StringHelper230.getHelperInfo();
        
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