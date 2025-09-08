public class KafkaProcessorTest {
    
    public static void main(String[] args) {
        KafkaProcessor processor = new KafkaProcessor();
        MessageHelper helper = new MessageHelper();
        
        // Test method functionality (now in helper)
        helper.processMessage20();
        
        // Test status
        String status = processor.getStatus();
        String helperStatus = helper.getHelperStatus();
        
        // Simple test validation
        int testsRun = 3;
        int testsPassed = 0;
        
        if ("processing".equals(status)) {
            testsPassed++;
        }
        
        if ("helper ready".equals(helperStatus)) {
            testsPassed++;
        }
        
        try {
            helper.processMessage20();
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