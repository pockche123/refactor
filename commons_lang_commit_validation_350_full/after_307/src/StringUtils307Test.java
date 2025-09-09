public class StringUtils307Test {
    
    public static void main(String[] args) {
        StringUtils307 utils = new StringUtils307();
        StringHelper307 helper = new StringHelper307();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils307.isEmpty("");
        String capitalized = StringUtils307.capitalize("hello");
        String reversed = StringHelper307.reverse("hello");
        String helperInfo = StringHelper307.getHelperInfo();
        
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