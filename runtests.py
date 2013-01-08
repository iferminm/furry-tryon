#coding=utf-8

## #############################################################
## Unnamed Social Lib
## Testing module
## Coded by: Israel Fermín Montilla <ferminster@gmail.com>
## Caracas - Venezuela (2013)
## #############################################################
from sys import argv
import unittest

def run_tests(test_directory='tests'):
    """
    Runs the tests contained on the specified
    directory
    """
    tests = unittest.defaultTestLoader.discover(test_directory)
    runner = unittest.TextTestRunner()
    runner.run(tests)

if __name__ == '__main__':
    if len(argv) == 1:
        run_tests()
    else:
        run_tests(test_directory=argv[1])
