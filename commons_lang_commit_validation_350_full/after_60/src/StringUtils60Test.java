public class StringUtils60Test {
    
    public static void main(String[] args) {
        StringUtils60 utils = new StringUtils60();
        StringHelper60 helper = new StringHelper60();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils60.isEmpty("");
        String capitalized = StringUtils60.capitalize("hello");
        String reversed = StringHelper60.reverse("hello");
        String helperInfo = StringHelper60.getHelperInfo();
        
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