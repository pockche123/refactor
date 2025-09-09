public class StringUtils121Test {
    
    public static void main(String[] args) {
        StringUtils121 utils = new StringUtils121();
        StringHelper121 helper = new StringHelper121();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils121.isEmpty("");
        String capitalized = StringUtils121.capitalize("hello");
        String reversed = StringHelper121.reverse("hello");
        String helperInfo = StringHelper121.getHelperInfo();
        
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