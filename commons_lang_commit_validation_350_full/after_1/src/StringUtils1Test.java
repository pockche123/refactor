public class StringUtils1Test {
    
    public static void main(String[] args) {
        StringUtils1 utils = new StringUtils1();
        StringHelper1 helper = new StringHelper1();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils1.isEmpty("");
        String capitalized = StringUtils1.capitalize("hello");
        String reversed = StringHelper1.reverse("hello");
        String helperInfo = StringHelper1.getHelperInfo();
        
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