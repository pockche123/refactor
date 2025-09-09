public class StringUtils128Test {
    
    public static void main(String[] args) {
        StringUtils128 utils = new StringUtils128();
        StringHelper128 helper = new StringHelper128();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils128.isEmpty("");
        String capitalized = StringUtils128.capitalize("hello");
        String reversed = StringHelper128.reverse("hello");
        String helperInfo = StringHelper128.getHelperInfo();
        
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