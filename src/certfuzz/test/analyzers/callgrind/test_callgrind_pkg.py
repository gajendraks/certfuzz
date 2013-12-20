'''
Created on Oct 24, 2012

@organization: cert.org
'''
import unittest
from certfuzz.test import misc
import certfuzz.analyzers.callgrind

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_api(self):
        module = certfuzz.analyzers.callgrind
        api_list = ['CallgrindAnnotateEmptyOutputFileError',
                    'CallgrindAnnotateError',
                    'CallgrindAnnotateMissingInputFileError',
                    'CallgrindAnnotateNoOutputFileError',
                    ]
        (is_fail, msg) = misc.check_for_apis(module, api_list)
        self.assertFalse(is_fail, msg)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
