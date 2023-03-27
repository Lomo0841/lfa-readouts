import unittest
from lfa_project.Test.ColorAveragorTest import ColorAveragorTest
from lfa_project.Test.DeepSearchTest import DeepSearchTest
from lfa_project.Test.FilterOnConditionsTest import FilterOnConditionsTest
from lfa_project.Test.HierarchicalSelectorTest import HierarchicalSelectorTest
from lfa_project.Test.MaxRGBTest import MaxRGBTest
from lfa_project.Test.GreyWorldTest import GreyWorldTest

if __name__ == '__main__':
        
    all_tests = unittest.TestSuite()
    all_tests.addTest(unittest.TestLoader().loadTestsFromTestCase(ColorAveragorTest))
    all_tests.addTest(unittest.TestLoader().loadTestsFromTestCase(DeepSearchTest))
    all_tests.addTest(unittest.TestLoader().loadTestsFromTestCase(FilterOnConditionsTest))
    all_tests.addTest(unittest.TestLoader().loadTestsFromTestCase(HierarchicalSelectorTest))
    all_tests.addTest(unittest.TestLoader().loadTestsFromTestCase(MaxRGBTest))
    all_tests.addTest(unittest.TestLoader().loadTestsFromTestCase(GreyWorldTest))
    unittest.TextTestRunner(verbosity=2).run(all_tests)

