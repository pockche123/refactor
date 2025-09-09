public class StringUtils54Test {
    
    public static void main(String[] args) {
        StringUtils54 utils = new StringUtils54();
        StringHelper54 helper = new StringHelper54();
        
        // Test functionality
        boolean isEmpty = StringUtils54.isEmpty("");
        String capitalized = StringUtils54.capitalize("hello");
        String reversed = StringUtils54.reverse("hello");
        String helperInfo = StringHelper54.getHelperInfo();
        
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