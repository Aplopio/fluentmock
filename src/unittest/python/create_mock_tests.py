#   fluentmock
#   Copyright 2013-2015 Michael Gruber
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

from mock import Mock
from hamcrest import assert_that, equal_to, instance_of
from fluentmock import UnitTests, create_mock


class CreateMockTests(UnitTests):

    def test_should_create_a_simple_mock(self):

        actual = create_mock()

        assert_that(actual, instance_of(Mock))

    def test_should_create_mock_with_property_from_given_keyword_argument(self):

        actual = create_mock(foo='bar')

        assert_that(actual.foo, equal_to('bar'))

    def test_should_create_mock_with_two_properties_when_two_properties_given(self):

        actual = create_mock(foo='bar', spam='eggs')

        assert_that(actual.foo, equal_to('bar'))
        assert_that(actual.spam, equal_to('eggs'))

    def test_should_create_mock_with_three_properties_when_three_properties_given(self):

        actual = create_mock(foo='bar', spam='eggs', hello='world')

        assert_that(actual.foo, equal_to('bar'))
        assert_that(actual.spam, equal_to('eggs'))

    def test_should_create_mock_using_given_specification(self):

        class SpecificationClass(object):
            pass

        actual = create_mock(SpecificationClass)

        assert_that(actual, instance_of(SpecificationClass))

    def test_should_create_mock_using_given_specification_and_properties(self):

        class SpecificationClass(object):
            pass

        actual = create_mock(SpecificationClass, bar='foo', eggs='spam')

        assert_that(actual, instance_of(SpecificationClass))
        assert_that(actual.bar, equal_to('foo'))
        assert_that(actual.eggs, equal_to('spam'))
