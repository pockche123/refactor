public class StringUtils229Test {
    
    public static void main(String[] args) {
        StringUtils229 utils = new StringUtils229();
        StringHelper229 helper = new StringHelper229();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils229.isEmpty("");
        String capitalized = StringUtils229.capitalize("hello");
        String reversed = StringHelper229.reverse("hello");
        String helperInfo = StringHelper229.getHelperInfo();
        
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