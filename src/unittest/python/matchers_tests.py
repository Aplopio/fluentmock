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

from fluentmock import UnitTests
from fluentmock.matchers import (AtLeastOnceMatcher,
                                 AnyValueMatcher,
                                 AnyValuesMatcher,
                                 AnyValueOfTypeMatcher,
                                 ContainsMatcher,
                                 FluentMatcher,
                                 ListContainsMatcher,
                                 NeverMatcher,
                                 TimesMatcher,
                                 a_list_containing,
                                 any_value_of_type,
                                 any_of,
                                 contains)
from fluentmock.exceptions import MatcherException
from hamcrest import assert_that, equal_to, instance_of


class FluentMatcherTests(UnitTests):

    def test_should_raise_exception_when_trying_to_match_value(self):

        matcher = FluentMatcher()

        self.assertRaises(NotImplementedError, matcher.matches, '1')

    def test_should_raise_exception_when_trying_to_get_string_representation(self):

        matcher = FluentMatcher()

        self.assertRaises(NotImplementedError, str, matcher)


class AnyArgumentMatcherTests(UnitTests):

    def test_should_return_true_when_string_is_given(self):

        matcher = AnyValueMatcher()

        actual = matcher.matches('hello world')

        assert_that(actual, equal_to(True))

    def test_should_return_true_when_integer_is_given(self):

        matcher = AnyValueMatcher()

        actual = matcher.matches(1)

        assert_that(actual, equal_to(True))

    def test_should_return_true_when_none_is_given(self):

        matcher = AnyValueMatcher()

        actual = matcher.matches(None)

        assert_that(actual, equal_to(True))

    def test_should_return_readable_string_representation(self):

        matcher = AnyValueMatcher()

        assert_that(str(matcher), equal_to('<< ANY_VALUE >>'))


class AnyArgumentsMatcherTests(UnitTests):

    def test_should_return_true_when_string_is_given(self):

        matcher = AnyValuesMatcher()

        actual = matcher.matches('hello world')

        assert_that(actual, equal_to(True))

    def test_should_return_true_when_integer_is_given(self):

        matcher = AnyValuesMatcher()

        actual = matcher.matches(1)

        assert_that(actual, equal_to(True))

    def test_should_return_true_when_none_is_given(self):

        matcher = AnyValuesMatcher()

        actual = matcher.matches(None)

        assert_that(actual, equal_to(True))

    def test_should_return_readable_string_representation(self):

        matcher = AnyValuesMatcher()

        assert_that(str(matcher), equal_to('<< ANY_VALUES >>'))


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


class NeverMatcherTests(UnitTests):

    def test_should_return_true_when_given_value_is_zero(self):

        matcher = NeverMatcher()

        assert_that(matcher.matches(0), equal_to(True))

    def test_should_return_false_when_given_value_is_not_zero(self):

        matcher = NeverMatcher()

        assert_that(matcher.matches(1), equal_to(False))
        assert_that(matcher.matches(2), equal_to(False))
        assert_that(matcher.matches(3), equal_to(False))

    def test_should_return_a_string_representation(self):

        matcher = NeverMatcher()

        assert_that(str(matcher)), equal_to('<< should never be called >>')


class AtLeastOnceMatcherTests(UnitTests):

    def test_should_return_true_when_given_value_is_one(self):

        matcher = AtLeastOnceMatcher()

        assert_that(matcher.matches(1), equal_to(True))

    def test_should_return_false_when_given_value_is_zero(self):

        matcher = AtLeastOnceMatcher()

        assert_that(matcher.matches(0), equal_to(False))

    def test_should_return_true_when_any_value_greater_than_one_is_given(self):

        matcher = AtLeastOnceMatcher()

        assert_that(matcher.matches(2), equal_to(True))
        assert_that(matcher.matches(3), equal_to(True))
        assert_that(matcher.matches(4), equal_to(True))

    def test_should_return_a_string_representation(self):

        matcher = AtLeastOnceMatcher()

        assert_that(str(matcher), equal_to("<< at least once >>"))


class TimesMatcherTests(UnitTests):

    def test_should_return_true_when_one_expected_and_one_given(self):

        matcher = TimesMatcher(1)

        assert_that(matcher.matches(1), equal_to(True))

    def test_should_return_false_when_one_expected_and_two_given(self):

        matcher = TimesMatcher(1)

        assert_that(matcher.matches(2), equal_to(False))

    def test_should_return_true_when_two_expected_and_two_given(self):

        matcher = TimesMatcher(2)

        assert_that(matcher.matches(2), equal_to(True))

    def test_should_return_string_representation(self):

        matcher = TimesMatcher(5)

        assert_that(str(matcher), equal_to('<< exactly 5 times >>'))


class AnyValueOfTypeMatcherTests(UnitTests):

    def test_should_return_true_when_asking_for_int_and_int_is_given(self):

        matcher = AnyValueOfTypeMatcher(int)

        assert_that(matcher.matches(1), equal_to(True))

    def test_should_return_false_when_asking_for_int_and_string_is_given(self):

        matcher = AnyValueOfTypeMatcher(int)

        assert_that(matcher.matches("Hello world"), equal_to(False))

    def test_should_return_true_when_asking_for_string_and_string_is_given(self):

        matcher = AnyValueOfTypeMatcher(str)

        assert_that(matcher.matches("Hello world!"), equal_to(True))

    def test_should_return_false_when_asking_for_string_and_int_is_given(self):

        matcher = AnyValueOfTypeMatcher(str)

        assert_that(matcher.matches(1), equal_to(False))

    def test_should_return_string_representation(self):

        matcher = AnyValueOfTypeMatcher(bool)

        assert_that(str(matcher), equal_to('<< Any value of type "bool" >>'))


class AnyValueOfTypeTests(UnitTests):

    def test_should_return_true_when_asking_for_int_and_int_is_given(self):

        matcher = any_value_of_type(int)

        assert_that(matcher.matches(1), equal_to(True))

    def test_should_return_false_when_asking_for_int_and_string_is_given(self):

        matcher = any_value_of_type(int)

        assert_that(matcher.matches("Hello world"), equal_to(False))

    def test_should_return_true_when_asking_for_string_and_string_is_given(self):

        matcher = any_value_of_type(str)

        assert_that(matcher.matches("Hello world!"), equal_to(True))

    def test_should_return_false_when_asking_for_string_and_int_is_given(self):

        matcher = any_value_of_type(str)

        assert_that(matcher.matches(1), equal_to(False))

    def test_should_return_string_representation(self):

        matcher = any_value_of_type(bool)

        assert_that(str(matcher), equal_to('<< Any value of type "bool" >>'))


class AnyOfMatcherTests(UnitTests):

    def test_should_raise_exception_when_no_argument_provided(self):

        self.assertRaises(MatcherException, any_of)

    def test_should_return_true_when_matching_one_element_and_one_element_is_given(self):

        matcher = any_of(1)

        assert_that(matcher.matches(1), equal_to(True))

    def tests_should_return_false_when_matching_one_element_but_list_has_another_element(self):

        matcher = any_of('a')

        assert_that(matcher.matches(1), equal_to(False))

    def test_should_return_true_when_two_elemens_given_and_matchin_one_of_them(self):

        matcher = any_of(1, 2)

        assert_that(matcher.matches(2), equal_to(True))

    def test_should_return_true_when_three_elemens_given_and_matchin_one_of_them(self):

        matcher = any_of('a', 1, 'b', 2)

        assert_that(matcher.matches('b'), equal_to(True))

    def test_should_return_string_representation(self):

        matcher = any_of(1, 2, 3)

        assert_that(str(matcher), equal_to('<< Any value in [1, 2, 3] >>'))


class ListContainsTests(UnitTests):

    def test_should_raise_exception_when_no_list_given(self):

        matcher = ListContainsMatcher('foo')

        self.assertRaises(MatcherException, matcher.matches, set([1, 2, 3]))

    def test_should_return_false_when_list_does_not_contain_element(self):

        matcher = ListContainsMatcher('foo')

        assert_that(matcher.matches([1, 2, 3]), equal_to(False))

    def test_should_return_true_when_list_is_expected_element(self):

        matcher = ListContainsMatcher('foo')

        assert_that(matcher.matches(['foo']), equal_to(True))

    def test_should_return_true_when_list_contains_expected_element(self):

        matcher = ListContainsMatcher('foo')

        assert_that(matcher.matches(['spam', 'foo']), equal_to(True))

    def test_should_return_string_representation(self):

        matcher = ListContainsMatcher('foo')

        assert_that(str(matcher), equal_to("<< a list containing element 'foo' >>"))


class AListContainingTests(UnitTests):

    def test_should_return_list_contains_matcher(self):

        matcher = a_list_containing('spam')

        assert_that(matcher, instance_of(ListContainsMatcher))

    def test_should_return_true_when_list_contains_element(self):

        matcher = a_list_containing('spam')

        assert_that(matcher.matches(['foo', 'spam']), equal_to(True))

    def test_should_return_false_when_list_does_not_contain_element(self):

        matcher = a_list_containing('bar')

        assert_that(matcher.matches(['foo', 'spam']), equal_to(False))
