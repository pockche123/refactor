public class StringUtils142Test {
    
    public static void main(String[] args) {
        StringUtils142 utils = new StringUtils142();
        StringHelper142 helper = new StringHelper142();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils142.isEmpty("");
        String capitalized = StringUtils142.capitalize("hello");
        String reversed = StringHelper142.reverse("hello");
        String helperInfo = StringHelper142.getHelperInfo();
        
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