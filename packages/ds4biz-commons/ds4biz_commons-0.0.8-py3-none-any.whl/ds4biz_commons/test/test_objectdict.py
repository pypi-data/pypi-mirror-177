from unittest.case import TestCase
from ds4biz_commons.utils.dict_utils import ObjectDict
class ObjectDictTest(TestCase):

    def test(self):
        
        o=ObjectDict()
        o.first_level.second_level.value=1
        self.assertEqual(type(o.first_level), ObjectDict)
        self.assertEqual(type(o.second_level), ObjectDict)
        self.assertEqual(o['first_level']['second_level']['value'], 1)
        self.assertEqual(o.first_level.second_level.value, 1)
        
    
    def test_conversion(self):
        
        obj={"a":{"b":1}}
        
        od=ObjectDict.convert(obj)
        self.assertEqual(od.a.b,1)
        self.assertEqual(type(od.a),ObjectDict)