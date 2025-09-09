public class StringUtils293Test {
    
    public static void main(String[] args) {
        StringUtils293 utils = new StringUtils293();
        StringHelper293 helper = new StringHelper293();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils293.isEmpty("");
        String capitalized = StringUtils293.capitalize("hello");
        String reversed = StringHelper293.reverse("hello");
        String helperInfo = StringHelper293.getHelperInfo();
        
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