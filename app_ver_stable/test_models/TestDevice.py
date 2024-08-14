import unittest
from models.devices import Device
from sqlalchemy.engine.row import Row

class TestDevice(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        devicemac = ["00:11:62:30:41:cd", "00:11:62:30:41:ac", "00:11:62:30:41:ab", "00:11:62:30:41:jk", "00:11:62:30:41:lm"] 
        print('setUpClass')
        for i in range(2,5):
            print("Entering " + devicemac[i] )
            Device.addDevice(devicemac[i], 1)
        

    @classmethod
    def tearDownClass(cls):
        devicemac = ["00:11:62:30:41:cd", "00:11:62:30:41:ac", "00:11:62:30:41:ab", "00:11:62:30:41:jk", "00:11:62:30:41:lm"]  
        print('teardownClass')
        for i in range(1,5):
            print("Deleting " + devicemac[i])
            Device.delDevice(devicemac[i])
   
    def setUp(self):
        print("setup")
        self.devicemac = ["00:11:62:30:41:cd", "00:11:62:30:41:ac", "00:11:62:30:41:ab", "00:11:62:30:41:jk", "00:11:62:30:41:lm"] 

    def tearDown(self):
        print("teardown")
        print('tearDown\n')
        
    def test_addDevice(self):
        
        # self.assertIsInstance(Device.addDevice(self.devicemac[0], 1), str)
        self.assertIsInstance(Device.addDevice(self.devicemac[1], 1), str)
        with self.assertRaises(ValueError):
            Device.addDevice("",  1)
			# with self.assertRaises(ValueError):
            Device.addDevice(self.devicemac[1], 0)
    
    def test_delDevice(self):
        # self.assertIsNone(Device.delDevice("FirstQueue1"))
        # self.assertIsInstance(Device.delDevice(self.devicemac[0]), int)
        
        with self.assertRaises(ValueError):
            Device.delDevice("")
    
    def test_getDevicePrintRequired(self):
        a, b, c = Device.getDevicePrintRequired(self.devicemac[0])
        print(a)
        print(b)
        print(c)
        self.assertIsInstance(Device.getDevicePrintRequired(self.devicemac[1]), Row)
        self.assertIsNone(Device.getDevicePrintRequired("FirstQueue1"))
        with self.assertRaises(ValueError):
            Device.getDevicePrintRequired("")  
    
    def test_getQueueIDandPrintingState(self):
        self.assertIsInstance(Device.getQueueIDandPrintingState(self.devicemac[1]), Row)
        self.assertIsNone(Device.getQueueIDandPrintingState("FirstQueue1"))
        with self.assertRaises(ValueError):
            Device.getQueueIDandPrintingState("")  
    
    def test_getDeviceOutputWidth(self):
        self.assertIsInstance(Device.getDeviceOutputWidth(self.devicemac[1]), Row)
        self.assertIsNone(Device.getDeviceOutputWidth("FirstQueue1"))
        with self.assertRaises(ValueError):
            Device.getDeviceOutputWidth("")  
    
    def test_setDeviceInfo(self):
        self.assertIsInstance(Device.setDeviceInfo(self.devicemac[1]), int)
        with self.assertRaises(ValueError):
            Device.setDeviceInfo("")  
    
    def test_setDeviceStatus(self):
        self.assertIsInstance(Device.setDeviceStatus(self.devicemac[1], ""), int)
        with self.assertRaises(ValueError):
            Device.setDeviceStatus("", "")  
    
    def test_setCompleteJob(self):
        self.assertIsInstance(Device.setDeviceStatus(self.devicemac[1], ""), int)
        with self.assertRaises(ValueError):
            Device.setDeviceStatus("", "")  
    
    def test_listDevices(self):
        self.assertIsInstance(Device.listDevices(), list)
    
    def test_setDevicePosition(self):
        pass
    
if __name__ =="__main__":
    unittest.main()