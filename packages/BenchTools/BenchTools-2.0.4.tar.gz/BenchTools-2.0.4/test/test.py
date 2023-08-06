from benchtools import addToBench, benchRound, clearRound
from unittest import TestCase, TestSuite, TextTestRunner, expectedFailure

def benchF():
    for i in range(10000000):
        x = 22/22/22/22/22

def benchFHard():
    for i in range(100000000):
        x = 22/22/22/22/22

class TestBenchmark(TestCase):
    
    def testSetOne(self):
        addToBench(benchF, "t-11", 1)
        
    def testSetAll(self):
        addToBench(benchF, "testetesteteste-12", 1)
        addToBench(benchF, "teste-14", 1)
        addToBench(benchF, "teste-15", 1)
        addToBench(benchF, "teste-16", 0)
        
    def testBench(self):
        benchRound()
    
    def testClear(self):
        clearRound()
        
    def testBenchWithLog(self):
        addToBench(benchF, "teste-22", 1)
        addToBench(benchFHard, "teste-24", 1)
        addToBench(benchF, "teste-25", 1)
        addToBench(benchF, "teste-26", 1)
        benchRound(True)
        clearRound()
        
    @expectedFailure
    def testSetNotCallable(self):
        addToBench(22, "t-11", 1)

def suite():
    suite = TestSuite()
    suite.addTest(TestBenchmark('testSetOne'))
    suite.addTest(TestBenchmark('testSetAll'))
    suite.addTest(TestBenchmark('testBench'))
    suite.addTest(TestBenchmark('testClear'))
    suite.addTest(TestBenchmark('testBenchWithLog'))
    suite.addTest(TestBenchmark('testSetNotCallable'))
    return suite

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
    