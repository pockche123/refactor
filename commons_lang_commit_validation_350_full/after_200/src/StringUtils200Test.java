public class StringUtils200Test {
    
    public static void main(String[] args) {
        StringUtils200 utils = new StringUtils200();
        StringHelper200 helper = new StringHelper200();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils200.isEmpty("");
        String capitalized = StringUtils200.capitalize("hello");
        String reversed = StringHelper200.reverse("hello");
        String helperInfo = StringHelper200.getHelperInfo();
        
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