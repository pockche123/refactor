public class StringUtils308Test {
    
    public static void main(String[] args) {
        StringUtils308 utils = new StringUtils308();
        StringHelper308 helper = new StringHelper308();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils308.isEmpty("");
        String capitalized = StringUtils308.capitalize("hello");
        String reversed = StringHelper308.reverse("hello");
        String helperInfo = StringHelper308.getHelperInfo();
        
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