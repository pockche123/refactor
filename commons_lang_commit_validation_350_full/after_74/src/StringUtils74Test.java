public class StringUtils74Test {
    
    public static void main(String[] args) {
        StringUtils74 utils = new StringUtils74();
        StringHelper74 helper = new StringHelper74();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils74.isEmpty("");
        String capitalized = StringUtils74.capitalize("hello");
        String reversed = StringHelper74.reverse("hello");
        String helperInfo = StringHelper74.getHelperInfo();
        
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