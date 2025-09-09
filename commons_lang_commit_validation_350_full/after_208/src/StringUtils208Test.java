public class StringUtils208Test {
    
    public static void main(String[] args) {
        StringUtils208 utils = new StringUtils208();
        StringHelper208 helper = new StringHelper208();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils208.isEmpty("");
        String capitalized = StringUtils208.capitalize("hello");
        String reversed = StringHelper208.reverse("hello");
        String helperInfo = StringHelper208.getHelperInfo();
        
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