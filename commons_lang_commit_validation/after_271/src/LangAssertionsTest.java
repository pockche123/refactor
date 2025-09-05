public class LangAssertionsTest {
    
    public static void main(String[] args) {
        int testsRun = 2;
        int testsPassed = 0;
        
        try {
            LangAssertions instance = new LangAssertions();
            testsPassed++;
            
            instance.assertNullPointerException(null);
            testsPassed++;
            
            System.out.println("Tests run: " + testsRun);
            System.out.println("Tests passed: " + testsPassed);
            System.out.println("Tests failed: " + (testsRun - testsPassed));
            
            if (testsPassed == testsRun) {
                System.out.println("ALL TESTS PASSED!");
                System.exit(0);
            } else {
                System.out.println("SOME TESTS FAILED!");
                System.exit(1);
            }
        } catch (Exception e) {
            System.out.println("Tests run: " + testsRun);
            System.out.println("Tests passed: 0");
            System.out.println("Tests failed: " + testsRun);
            System.out.println("TESTS FAILED: " + e.getMessage());
            System.exit(1);
        }
    }
}