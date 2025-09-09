public class StringUtils187Test {
    
    public static void main(String[] args) {
        StringUtils187 utils = new StringUtils187();
        StringHelper187 helper = new StringHelper187();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils187.isEmpty("");
        String capitalized = StringUtils187.capitalize("hello");
        String reversed = StringHelper187.reverse("hello");
        String helperInfo = StringHelper187.getHelperInfo();
        
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