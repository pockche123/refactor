public class StringUtils97Test {
    
    public static void main(String[] args) {
        StringUtils97 utils = new StringUtils97();
        StringHelper97 helper = new StringHelper97();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils97.isEmpty("");
        String capitalized = StringUtils97.capitalize("hello");
        String reversed = StringHelper97.reverse("hello");
        String helperInfo = StringHelper97.getHelperInfo();
        
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