public class StringUtils6Test {
    
    public static void main(String[] args) {
        StringUtils6 utils = new StringUtils6();
        StringHelper6 helper = new StringHelper6();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils6.isEmpty("");
        String capitalized = StringUtils6.capitalize("hello");
        String reversed = StringHelper6.reverse("hello");
        String helperInfo = StringHelper6.getHelperInfo();
        
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