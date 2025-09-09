public class SpringService166Test {
    
    public static void main(String[] args) {
        SpringService166 service = new SpringService166();
        
        // Test functionality
        service.processData();
        String status = service.getStatus();
        
        // Simple validation
        int testsRun = 2;
        int testsPassed = 0;
        
        if ("active".equals(status)) {
            testsPassed++;
        }
        
        try {
            service.processData();
            testsPassed++;
        } catch (Exception e) {
            // Test failed
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