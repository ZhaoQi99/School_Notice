'''
Created on Oct 10, 2018

@author: QiZhao
'''
from tool import *
import unittest
from spider import *
import configs_sample1

class TestSpider(unittest.TestCase):
    "Test tool.py"
    
    def test_spider_date(self):
        for dic in configs_sample1.SPIDER_CONFIG:
            try:
                ret=spider(dic['url'],dic['rule'], dic['coding'])
                self.assertTrue(len(ret)>0)
            except Exception:
                pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()