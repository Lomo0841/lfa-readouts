import unittest
from lfa_project.Test.ColorAveragorTest import ColorAveragorTest
from lfa_project.Test.DeepSearchTest import DeepSearchTest
from lfa_project.Test.FilterOnConditionsTest import FilterOnConditionsTest
from lfa_project.Test.HierarchicalSelectorTest import HierarchicalSelectorTest

if __name__ == '__main__':
        
    all_tests = unittest.TestSuite()
    all_tests.addTest(unittest.TestLoader().loadTestsFromTestCase(ColorAveragorTest))
    all_tests.addTest(unittest.TestLoader().loadTestsFromTestCase(DeepSearchTest))
    all_tests.addTest(unittest.TestLoader().loadTestsFromTestCase(FilterOnConditionsTest))
    all_tests.addTest(unittest.TestLoader().loadTestsFromTestCase(HierarchicalSelectorTest))

    unittest.TextTestRunner(verbosity=2).run(all_tests)

