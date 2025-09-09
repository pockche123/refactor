public class StringUtils35Test {
    
    public static void main(String[] args) {
        StringUtils35 utils = new StringUtils35();
        StringHelper35 helper = new StringHelper35();
        
        // Test functionality (reverse method now in helper)
        boolean isEmpty = StringUtils35.isEmpty("");
        String capitalized = StringUtils35.capitalize("hello");
        String reversed = StringHelper35.reverse("hello");
        String helperInfo = StringHelper35.getHelperInfo();
        
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