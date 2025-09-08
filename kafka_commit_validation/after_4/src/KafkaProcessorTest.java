public class KafkaProcessorTest {
    
    public static void main(String[] args) {
        KafkaProcessor processor = new KafkaProcessor();
        
        // Test method functionality
        processor.processKafkaMessage4();
        
        // Test status
        String status = processor.getStatus();
        
        // Simple test validation
        int testsRun = 2;
        int testsPassed = 0;
        
        if ("processing".equals(status)) {
            testsPassed++;
        }
        
        try {
            processor.processKafkaMessage4();
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