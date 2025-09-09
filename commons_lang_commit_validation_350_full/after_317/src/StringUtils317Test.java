public class StringUtils317Test {
    
    public static void main(String[] args) {
        StringUtils317 utils = new StringUtils317();
        StringHelper317 helper = new StringHelper317();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils317.isEmpty("");
        String capitalized = StringUtils317.capitalize("hello");
        String reversed = StringHelper317.reverse("hello");
        String helperInfo = StringHelper317.getHelperInfo();
        
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