from ReferenceResolver.Tests import ResolveTestCase
import sys
import unittest
import argparse
from log import setup_logging
setup_logging(log_level="warn")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run unit tests")
    parser.add_argument('--log-filename', action='store', help='Filename where output will be written (e.g., ReferenceResolver/Tests/output/unit_tests_log.txt)')
    parser.add_argument('unittest_args', nargs='*')
    args = parser.parse_args()

    sys.argv[1:] = args.unittest_args

    if args.log_filename is not None:
        print("Output will be written to {}".format(args.log_filename))
        f = open(args.log_filename, "w")
        runner = unittest.TextTestRunner(f)
        unittest.main(testRunner=runner)
        f.close()
    else:
        unittest.main()

