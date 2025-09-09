public class StringUtils304Test {
    
    public static void main(String[] args) {
        StringUtils304 utils = new StringUtils304();
        StringHelper304 helper = new StringHelper304();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils304.isEmpty("");
        String capitalized = StringUtils304.capitalize("hello");
        String reversed = StringHelper304.reverse("hello");
        String helperInfo = StringHelper304.getHelperInfo();
        
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