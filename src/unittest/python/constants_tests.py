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

from fluentmock import (ANY_INTEGER,
                        ANY_STRING,
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
