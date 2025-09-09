public class StringUtils242Test {
    
    public static void main(String[] args) {
        StringUtils242 utils = new StringUtils242();
        StringHelper242 helper = new StringHelper242();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils242.isEmpty("");
        String capitalized = StringUtils242.capitalize("hello");
        String reversed = StringHelper242.reverse("hello");
        String helperInfo = StringHelper242.getHelperInfo();
        
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