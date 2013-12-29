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

from hamcrest import assert_that, equal_to
from fluentmock import UnitTests, when, verify

import targetpackage


class ExampleTest(UnitTests):

    def test_should_return_configured_value_three_when_called_and_verify_it_has_been_called(self):

        when(targetpackage).targetfunction(2).then_return(3)

        assert_that(targetpackage.targetfunction(2), equal_to(3))

        verify(targetpackage).targetfunction(2)
