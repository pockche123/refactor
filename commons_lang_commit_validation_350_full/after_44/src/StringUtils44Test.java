public class StringUtils44Test {
    
    public static void main(String[] args) {
        StringUtils44 utils = new StringUtils44();
        StringHelper44 helper = new StringHelper44();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils44.isEmpty("");
        String capitalized = StringUtils44.capitalize("hello");
        String reversed = StringHelper44.reverse("hello");
        String helperInfo = StringHelper44.getHelperInfo();
        
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