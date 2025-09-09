public class StringUtils286Test {
    
    public static void main(String[] args) {
        StringUtils286 utils = new StringUtils286();
        StringHelper286 helper = new StringHelper286();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils286.isEmpty("");
        String capitalized = StringUtils286.capitalize("hello");
        String reversed = StringHelper286.reverse("hello");
        String helperInfo = StringHelper286.getHelperInfo();
        
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