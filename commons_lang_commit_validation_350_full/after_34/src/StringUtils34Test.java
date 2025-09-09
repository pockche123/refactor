public class StringUtils34Test {
    
    public static void main(String[] args) {
        StringUtils34 utils = new StringUtils34();
        StringHelper34 helper = new StringHelper34();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils34.isEmpty("");
        String capitalized = StringUtils34.capitalize("hello");
        String reversed = StringHelper34.reverse("hello");
        String helperInfo = StringHelper34.getHelperInfo();
        
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