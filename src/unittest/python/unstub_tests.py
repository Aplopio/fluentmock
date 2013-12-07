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

from hamcrest import assert_that, equal_to
from fluentmock import when, unstub, get_stubs

import targetpackage


class UnstubTests(TestCase):

    def should_unstub_stubbed_function(self):

        when(targetpackage).stub_test_1().then_return('stubbed!')

        unstub()

        assert_that(targetpackage.stub_test_1(), equal_to('not stubbed 1'))

    def should_unstub_multiple_stubbed_function(self):

        when(targetpackage).stub_test_1().then_return('stubbed call! 1')
        when(targetpackage).stub_test_2().then_return('stubbed call! 2')

        unstub()

        assert_that('not stubbed 1', equal_to(targetpackage.stub_test_1()))
        assert_that('not stubbed 2', equal_to(targetpackage.stub_test_2()))

    def should_reset_list_of_stubs(self):

        when(targetpackage).stub_test_1().then_return('stubbed call! 1')
        when(targetpackage).stub_test_2().then_return('stubbed call! 2')

        unstub()

        assert_that([], equal_to(get_stubs()))
