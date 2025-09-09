public class StringUtils298Test {
    
    public static void main(String[] args) {
        StringUtils298 utils = new StringUtils298();
        StringHelper298 helper = new StringHelper298();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils298.isEmpty("");
        String capitalized = StringUtils298.capitalize("hello");
        String reversed = StringHelper298.reverse("hello");
        String helperInfo = StringHelper298.getHelperInfo();
        
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