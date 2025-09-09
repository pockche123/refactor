public class StringUtils138Test {
    
    public static void main(String[] args) {
        StringUtils138 utils = new StringUtils138();
        StringHelper138 helper = new StringHelper138();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils138.isEmpty("");
        String capitalized = StringUtils138.capitalize("hello");
        String reversed = StringHelper138.reverse("hello");
        String helperInfo = StringHelper138.getHelperInfo();
        
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