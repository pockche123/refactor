public class StringUtils252Test {
    
    public static void main(String[] args) {
        StringUtils252 utils = new StringUtils252();
        StringHelper252 helper = new StringHelper252();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils252.isEmpty("");
        String capitalized = StringUtils252.capitalize("hello");
        String reversed = StringHelper252.reverse("hello");
        String helperInfo = StringHelper252.getHelperInfo();
        
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