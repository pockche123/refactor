public class StringUtils231Test {
    
    public static void main(String[] args) {
        StringUtils231 utils = new StringUtils231();
        StringHelper231 helper = new StringHelper231();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils231.isEmpty("");
        String capitalized = StringUtils231.capitalize("hello");
        String reversed = StringHelper231.reverse("hello");
        String helperInfo = StringHelper231.getHelperInfo();
        
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