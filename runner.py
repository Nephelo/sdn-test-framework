# Copyright (c) 2015,
# Philipp Hertweck
#
# This code is provided under the BSD 2-Clause License.
# Please refer to the LICENSE.txt file for further information.


import unittest

loader = unittest.TestLoader()
tests = loader.discover('./')

testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)