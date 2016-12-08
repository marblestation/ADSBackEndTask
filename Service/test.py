from ReferenceResolver.Tests import ResolveTestCase
import unittest

if __name__ == '__main__':
    log_file = 'ReferenceResolver/Tests/output/unit_tests_log.txt'
    f = open(log_file, "w")
    runner = unittest.TextTestRunner(f)
    unittest.main(testRunner=runner)
    f.close()
    print("Output written to {}".format(log_file))
