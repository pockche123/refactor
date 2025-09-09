public class StringUtils326Test {
    
    public static void main(String[] args) {
        StringUtils326 utils = new StringUtils326();
        StringHelper326 helper = new StringHelper326();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils326.isEmpty("");
        String capitalized = StringUtils326.capitalize("hello");
        String reversed = StringHelper326.reverse("hello");
        String helperInfo = StringHelper326.getHelperInfo();
        
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