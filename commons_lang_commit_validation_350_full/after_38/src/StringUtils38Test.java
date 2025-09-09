public class StringUtils38Test {
    
    public static void main(String[] args) {
        StringUtils38 utils = new StringUtils38();
        StringHelper38 helper = new StringHelper38();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils38.isEmpty("");
        String capitalized = StringUtils38.capitalize("hello");
        String reversed = StringHelper38.reverse("hello");
        String helperInfo = StringHelper38.getHelperInfo();
        
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