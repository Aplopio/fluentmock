#   fluentmock
#   Copyright 2013 Michael Gruber
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from unittest import TestCase

from fluentmock import when, unstub, get_stubs

import targetpackage


class UnstubTests(TestCase):

    def test_should_unstub_stubbed_function(self):

        when(targetpackage).stub_test_1().then_return('stubbed!')

        unstub()

        self.assertEqual('not stubbed 1', targetpackage.stub_test_1())

    def test_should_unstub_multiple_stubbed_function(self):

        when(targetpackage).stub_test_1().then_return('stubbed call! 1')
        when(targetpackage).stub_test_2().then_return('stubbed call! 2')

        unstub()

        self.assertEqual('not stubbed 1', targetpackage.stub_test_1())
        self.assertEqual('not stubbed 2', targetpackage.stub_test_2())

    def test_should_reset_list_of_stubs(self):

        when(targetpackage).stub_test_1().then_return('stubbed call! 1')
        when(targetpackage).stub_test_2().then_return('stubbed call! 2')

        unstub()

        self.assertEqual([], get_stubs())
