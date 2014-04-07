#   fluentmock
#   Copyright 2013-2014 Michael Gruber
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

from fluentmock import (ANY_BOOLEAN,
                        ANY_FLOAT,
                        ANY_INTEGER,
                        ANY_LIST,
                        ANY_LONG,
                        ANY_STRING,
                        ANY_TUPLE,
                        ANY_UNICODE,
                        ANY_VALUE,
                        ANY_VALUES,
                        UnitTests,
                        when)
from hamcrest import assert_that, equal_to

import targetpackage


class MatcherTests(UnitTests):

    def test_should_match_any_value(self):

        when(targetpackage).targetfunction(ANY_VALUE).then_return('Matched!')

        assert_that(targetpackage.targetfunction(123), equal_to('Matched!'))

    def test_should_match_any_values(self):

        when(targetpackage).targetfunction(ANY_VALUES).then_return('Matched!')

        assert_that(targetpackage.targetfunction(1, 2, 3), equal_to('Matched!'))

    def test_should_match_any_integer(self):

        when(targetpackage).targetfunction(ANY_INTEGER).then_return('Yes!')

        assert_that(targetpackage.targetfunction(2), equal_to('Yes!'))

    def test_should_match_any_string(self):

        when(targetpackage).targetfunction(ANY_STRING).then_return('Yes!')

        assert_that(targetpackage.targetfunction('Hello world'), equal_to('Yes!'))

    def test_should_match_any_boolean(self):

        when(targetpackage).targetfunction(ANY_BOOLEAN).then_return('Yes!')

        assert_that(targetpackage.targetfunction(True), equal_to('Yes!'))
        assert_that(targetpackage.targetfunction(False), equal_to('Yes!'))

    def test_should_match_any_long(self):

        when(targetpackage).targetfunction(ANY_LONG).then_return('Yes!')

        assert_that(targetpackage.targetfunction(123L), equal_to('Yes!'))

    def test_should_match_any_float(self):

        when(targetpackage).targetfunction(ANY_FLOAT).then_return('Yes!')

        assert_that(targetpackage.targetfunction(1.23), equal_to('Yes!'))

    def test_should_match_any_unicode(self):

        when(targetpackage).targetfunction(ANY_UNICODE).then_return('Yes!')

        assert_that(targetpackage.targetfunction(u'spam eggs'), equal_to('Yes!'))

    def test_should_match_any_tuple(self):

        when(targetpackage).targetfunction(ANY_TUPLE).then_return('Yes!')

        assert_that(targetpackage.targetfunction((1, 2, 3, 4, 5)), equal_to('Yes!'))

    def test_should_match_any_list(self):

        when(targetpackage).targetfunction(ANY_LIST).then_return('Yes!')

        assert_that(targetpackage.targetfunction(['a', 'b', 'c']), equal_to('Yes!'))
