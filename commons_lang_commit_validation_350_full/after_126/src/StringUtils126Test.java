public class StringUtils126Test {
    
    public static void main(String[] args) {
        StringUtils126 utils = new StringUtils126();
        StringHelper126 helper = new StringHelper126();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils126.isEmpty("");
        String capitalized = StringUtils126.capitalize("hello");
        String reversed = StringHelper126.reverse("hello");
        String helperInfo = StringHelper126.getHelperInfo();
        
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