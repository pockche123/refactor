public class StringUtils184Test {
    
    public static void main(String[] args) {
        StringUtils184 utils = new StringUtils184();
        StringHelper184 helper = new StringHelper184();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils184.isEmpty("");
        String capitalized = StringUtils184.capitalize("hello");
        String reversed = StringHelper184.reverse("hello");
        String helperInfo = StringHelper184.getHelperInfo();
        
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