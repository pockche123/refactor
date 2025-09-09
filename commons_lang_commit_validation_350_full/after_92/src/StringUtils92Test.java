public class StringUtils92Test {
    
    public static void main(String[] args) {
        StringUtils92 utils = new StringUtils92();
        StringHelper92 helper = new StringHelper92();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils92.isEmpty("");
        String capitalized = StringUtils92.capitalize("hello");
        String reversed = StringHelper92.reverse("hello");
        String helperInfo = StringHelper92.getHelperInfo();
        
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