public class StringUtils110Test {
    
    public static void main(String[] args) {
        StringUtils110 utils = new StringUtils110();
        StringHelper110 helper = new StringHelper110();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils110.isEmpty("");
        String capitalized = StringUtils110.capitalize("hello");
        String reversed = StringHelper110.reverse("hello");
        String helperInfo = StringHelper110.getHelperInfo();
        
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