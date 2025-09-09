public class StringUtils250Test {
    
    public static void main(String[] args) {
        StringUtils250 utils = new StringUtils250();
        StringHelper250 helper = new StringHelper250();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils250.isEmpty("");
        String capitalized = StringUtils250.capitalize("hello");
        String reversed = StringHelper250.reverse("hello");
        String helperInfo = StringHelper250.getHelperInfo();
        
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