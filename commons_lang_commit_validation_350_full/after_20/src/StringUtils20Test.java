public class StringUtils20Test {
    
    public static void main(String[] args) {
        StringUtils20 utils = new StringUtils20();
        StringHelper20 helper = new StringHelper20();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils20.isEmpty("");
        String capitalized = StringUtils20.capitalize("hello");
        String reversed = StringHelper20.reverse("hello");
        String helperInfo = StringHelper20.getHelperInfo();
        
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