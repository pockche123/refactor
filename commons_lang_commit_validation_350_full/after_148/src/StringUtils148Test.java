public class StringUtils148Test {
    
    public static void main(String[] args) {
        StringUtils148 utils = new StringUtils148();
        StringHelper148 helper = new StringHelper148();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils148.isEmpty("");
        String capitalized = StringUtils148.capitalize("hello");
        String reversed = StringHelper148.reverse("hello");
        String helperInfo = StringHelper148.getHelperInfo();
        
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