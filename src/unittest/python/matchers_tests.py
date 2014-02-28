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

from fluentmock import UnitTests
from fluentmock.matchers import ContainsMatcher, FluentAnyArgument, FluentAnyArguments, FluentMatcher, contains
from hamcrest import assert_that, equal_to, instance_of


class FluentMatcherTests(UnitTests):

    def test_should_raise_exception_when_trying_to_match_value(self):

        matcher = FluentMatcher()

        self.assertRaises(NotImplementedError, matcher.matches, '1')

    def test_should_raise_exception_when_trying_to_get_string_representation(self):

        matcher = FluentMatcher()

        self.assertRaises(NotImplementedError, str, matcher)


class FluentAnyArgumentTests(UnitTests):

    def test_should_return_true_when_string_is_given(self):

        matcher = FluentAnyArgument()

        actual = matcher.matches('hello world')

        assert_that(actual, equal_to(True))

    def test_should_return_true_when_integer_is_given(self):

        matcher = FluentAnyArgument()

        actual = matcher.matches(1)

        assert_that(actual, equal_to(True))

    def test_should_return_true_when_none_is_given(self):

        matcher = FluentAnyArgument()

        actual = matcher.matches(None)

        assert_that(actual, equal_to(True))

    def test_should_return_readable_string_representation(self):

        matcher = FluentAnyArgument()

        assert_that(str(matcher), equal_to('<< ANY_ARGUMENT >>'))


class FluentAnyArgumentsTests(UnitTests):

    def test_should_return_true_when_string_is_given(self):

        matcher = FluentAnyArguments()

        actual = matcher.matches('hello world')

        assert_that(actual, equal_to(True))

    def test_should_return_true_when_integer_is_given(self):

        matcher = FluentAnyArguments()

        actual = matcher.matches(1)

        assert_that(actual, equal_to(True))

    def test_should_return_true_when_none_is_given(self):

        matcher = FluentAnyArguments()

        actual = matcher.matches(None)

        assert_that(actual, equal_to(True))

    def test_should_return_readable_string_representation(self):

        matcher = FluentAnyArguments()

        assert_that(str(matcher), equal_to('<< ANY_ARGUMENTS >>'))


class ContainsMatcherTests(UnitTests):

    def test_should_return_true_when_string_contains_substring(self):

        matcher = ContainsMatcher('foo')

        assert_that(matcher.matches('spam foo bar eggs'), equal_to(True))

    def test_should_return_false_when_string_does_not_contain_substring(self):

        matcher = ContainsMatcher('foo')

        assert_that(matcher.matches('spam eggs'), equal_to(False))

    def test_should_return_true_when_string_is_equal_to_substring(self):

        matcher = ContainsMatcher('foo')

        assert_that(matcher.matches('foo'), equal_to(True))


class ContainsTests(UnitTests):

    def test_should_create_a_new_contains_matcher(self):

        matcher = contains('eggs')

        assert_that(matcher, instance_of(ContainsMatcher))

    def test_should_create_a_matcher_for_given_substring(self):

        matcher = contains('eggs')

        assert_that(matcher.matches('spam eggs'), equal_to(True))

    def test_should_return_a_string_representation(self):

        matcher = contains('eggs')

        assert_that(str(matcher), equal_to('<< a string containing "eggs" >>'))
