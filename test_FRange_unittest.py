#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 08:57:32 2019

@author: nathan
"""

import unittest
from FRange import FRange

testObject1 = FRange((2,3,"()"))
testObject2 = FRange([4,5,"[]"])
testObject3 = FRange(((2,3,"()"),[4,5,"[]"]))
testObject4 = FRange((2,3,"()"))
testObject5 = FRange((2,3,"()"))
testObject6 = FRange((2,3,"()"))
testObject7 = FRange((2,3,"()"))
testObject8 = FRange((2,3,"()"))
testObject9 = FRange((2,3,"()"))
testObject10 = FRange((2,3,"()"))
testObject11 = FRange((2,3,"()"))
testObject12 = FRange((2,3,"[]"))
testObject13 = FRange(((2,3,"()"), (4,5,"[]"), (6,7,"()")))
testObject14 = FRange(((2,3,"()"), (4,5,"[]"), (6,7,"()")))

class test_FRange(unittest.TestCase):
    def testCreateRange(self):
        self.assertEqual(testObject1.value(), "(2,3)", "Should be (2,3)")
        self.assertEqual(testObject2.value(), "[4,5]", "Should be [4,5]")
        self.assertEqual(testObject3.value(), "(2,3)\u222a[4,5]", 
                         "Should be (2,3)\u222a[4,5]")
    def testUnion(self):
        testObject4.union((6,7,"(]"))
        self.assertEqual(testObject4.value(), "(2,3)\u222a(6,7]",
                        "Should be (2,3)\u222a(6,7]")
    def testUnionDuplicate(self):
        testObject5.union((2,3,"()"))
        self.assertEqual(testObject5.value(), "(2,3)",
                         "Should be (2,3)")
    def testUnionOverwrite(self):
        testObject6.union((2,3,"(]"))
        self.assertEqual(testObject6.value(), "(2,3]",
                        "Should be (2,3]")
    def testUnionExtend(self):
        testObject7.union((3,4,"[]"))
        self.assertEqual(testObject7.value(), "(2,4]",
                        "Should be (2,4]")
    def testUnionExtendMinusOne(self):
        testObject8.union((3,6,"(]"))
        self.assertEqual(testObject8.value(), "(2,3)\u222a(3,6]",
                        "Should be (2,3)\u222a(3,6]")
    def testUnionMultiple(self):
        testObject9.union(((3,4,"()"), [5,6,"[]"]))
        self.assertEqual(testObject9.value(), "(2,3)\u222a(3,4)\u222a[5,6]",
                         "Should be (2,3)\u222a(3,4)\u222a[5,6]")
    def testIntersect(self):
        testObject10.intersect((2.25,3,"(]"))
        self.assertEqual(testObject10.value(), "(2.25,3)", "Should be (2.25,3)")
    def testIntersectDuplicate(self):
        testObject11.intersect((2,3,"()"))
        self.assertEqual(testObject11.value(), "(2,3)", "Should be (2,3)")
    def testIntersectOverwrite(self):
        testObject12.intersect((2,3,"()"))
        self.assertEqual(testObject12.value(), "(2,3)", "Should be (2,3)")
    def testIntersectMultiple(self):
        testObject13.intersect(((2.5,3.5,"[)"), (4,9,"(]")))
        self.assertEqual(testObject13.value(), "[2.5,3)\u222a(4,5]\u222a(6,7)",
                         "Should be [2.5,3)\u222a(4,5]\u222a(6,7)")
    def testIntersectDropRange(self):
        testObject14.intersect((4,7,"()"))
        self.assertEqual(testObject14.value(), "(4,5]\u222a(6,7)",
                        "Should be (4,5]\u222a(6,7)")
if __name__=='__main__':
    unittest.main()
    