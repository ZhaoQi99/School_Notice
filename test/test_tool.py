'''
Created on Oct 10, 2018

@author: QiZhao
'''
from tool import *
import unittest

class TestTool(unittest.TestCase):
    "Test tool.py"
    
    def test_Mkdir(self):
        temp=os.getcwd()
        self.assertEqual(False,os.path.exists(temp+"/test1"))
        Mkdir("test1")
        self.assertNotEqual(False,os.path.exists(temp+"/test1"))
    
    def test_Mkfile(self):
        temp=os.getcwd()
        self.assertEqual(False,os.path.exists(temp+"/test.in"))
        Mkfile("test.in")
        self.assertNotEqual(False,os.path.exists(temp+"/test.in"))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()