# from types import NoneType
import unittest
from app_ver_1.models.queues import Queue
from sqlalchemy.engine.row import Row

class TestQueue(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('setupClass')

    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        print('setUp')
        for i in range(1,10):
            Queue.addQueue("FirstQueue")
            # self.test_addQueue()
        
    def tearDown(self):
        print('tearDown\n')

    def test_addQueue(self):
        with self.assertRaises(ValueError):
            Queue.addQueue("")
        self.assertIsInstance(Queue.addQueue("FirstQueue"), int)
        
    def test_delQueue(self):
        self.assertIsInstance(Queue.delQueue(3), int)
        with self.assertRaises(ValueError):
            Queue.delQueue("")
        # with self.assertRaises(ValueError):
            Queue.delQueue("x")
    
    def test_updatePosition(self):
        self. assertIsInstance(Queue.updatePosition(5), int)
        with self.assertRaises(ValueError):
            Queue.updatePosition("x")
        # with self.assertRaises(ValueError):
            Queue.updatePosition("")
               
    def test_resetQueue(self):
        with self.assertRaises(ValueError):
            Queue.resetQueue("x")
        # with self.assertRaises(ValueError):
            Queue.resetQueue("") 
        self.assertIsInstance(Queue.resetQueue(4), int)
    
    def test_getQueuePrintParameters(self):
        # data = Queue.getQueuePrintParameters(100)
        # print(type(data))
        # print(data.logo)
        self.assertIsInstance(Queue.getQueuePrintParameters(56), Row)
        self.assertIsNone(Queue.getQueuePrintParameters(2000))
        with self.assertRaises(ValueError):
            Queue.getQueuePrintParameters("x")
        # with self.assertRaises(ValueError):
            Queue.getQueuePrintParameters("")  
            
    def test_getPosition(self):
        # print("Verification Item value")
        # print(Queue.getPosition(400))
        self.assertIsInstance(Queue.getPosition(56), int)
        self.assertIsNone(Queue.getPosition(1000))
        with self.assertRaises(ValueError):
            Queue.getQueuePrintParameters("x")
        # with self.assertRaises(ValueError):
            Queue.getQueuePrintParameters("")  
    
    def test_listQueues(self):
        self.assertIsInstance(Queue.listQueues(), list)

if __name__ == "__main__":
    unittest.main()