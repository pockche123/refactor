public class KafkaProcessor4Test {
    
    public static void main(String[] args) {
        KafkaProcessor4 processor = new KafkaProcessor4();
        
        // Test functionality
        processor.processMessage();
        String status = processor.getStatus();
        
        // Simple validation
        int testsRun = 2;
        int testsPassed = 0;
        
        if ("processing".equals(status)) {
            testsPassed++;
        }
        
        try {
            processor.processMessage();
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