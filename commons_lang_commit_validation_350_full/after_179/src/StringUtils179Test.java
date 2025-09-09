public class StringUtils179Test {
    
    public static void main(String[] args) {
        StringUtils179 utils = new StringUtils179();
        StringHelper179 helper = new StringHelper179();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils179.isEmpty("");
        String capitalized = StringUtils179.capitalize("hello");
        String reversed = StringHelper179.reverse("hello");
        String helperInfo = StringHelper179.getHelperInfo();
        
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