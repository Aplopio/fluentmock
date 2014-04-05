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

from mock import Mock
from hamcrest import assert_that, equal_to
from fluentmock import (ANY_ARGUMENT,
                        ANY_ARGUMENTS,
                        NEVER,
                        UnitTests,
                        when,
                        verify)

from fluentmock.exceptions import (FoundMatcherInNativeVerificationError,
                                   InvalidAttributeError,
                                   InvalidUseOfAnyArgumentsError,
                                   VerificationError)

import targetpackage


class VerifyTests(UnitTests):

    def test_should_verify_a_simple_call(self):

        when(targetpackage).targetfunction().then_return('123')

        targetpackage.targetfunction()

        verify(targetpackage).targetfunction()

    def test_should_verify_a_simple_call_when_addressing_using_strings(self):

        when('targetpackage').targetfunction().then_return('123')

        targetpackage.targetfunction()

        verify('targetpackage').targetfunction()

    def test_should_raise_exception_when_target_does_not_have_attribute(self):

        when(targetpackage).targetfunction().then_return('123')

        targetpackage.targetfunction()

        exception_raised = False
        try:
            verify(targetpackage).spameggs
        except InvalidAttributeError as error:
            exception_raised = True
            self.assertEqual('The target "targetpackage" has no attribute called "spameggs".', str(error))

        assert_that(exception_raised)

    def test_should_verify_a_simple_call_with_a_argument(self):

        when(targetpackage).targetfunction(1).then_return('123')

        targetpackage.targetfunction(1)

        verify(targetpackage).targetfunction(1)

    def test_should_raise_error_when_function_patched_and_not_called_with_expected_argument(self):

        when(targetpackage).targetfunction(1).then_return('123')

        targetpackage.targetfunction(2)

        exception_raised = False
        try:
            verify(targetpackage).targetfunction(1)
        except VerificationError as error:
            exception_raised = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.targetfunction(1) << at least once >>
 but was: call targetpackage.targetfunction(2)
"""))

        assert_that(exception_raised)

    def test_should_verify_a_call_with_multiple_arguments(self):

        when(targetpackage).targetfunction(1, 2).then_return('123')

        targetpackage.targetfunction(1, 2)

        verify(targetpackage).targetfunction(1, 2)

    def test_should_raise_error_when_function_patched_and_not_called_with_expected_arguments(self):

        when(targetpackage).targetfunction(1, 2).then_return('123')

        targetpackage.targetfunction(2, 1)

        exception_raised = False
        try:
            verify(targetpackage).targetfunction(1, 2)
        except VerificationError as error:
            exception_raised = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.targetfunction(1, 2) << at least once >>
 but was: call targetpackage.targetfunction(2, 1)
"""))

        assert_that(exception_raised)

    def test_should_raise_error_when_function_not_called_with_expected_arguments_but_in_other_ways(self):

        when(targetpackage).targetfunction(1, 2).then_return('123')

        targetpackage.targetfunction('abc', 123, True)
        targetpackage.targetfunction('spam', 2, 1, 'eggs', False)

        exception_raised = False
        try:
            verify(targetpackage).targetfunction(1, 2)
        except VerificationError as error:
            exception_raised = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.targetfunction(1, 2) << at least once >>
 but was: call targetpackage.targetfunction('abc', 123, True)
          call targetpackage.targetfunction('spam', 2, 1, 'eggs', False)
"""))

        assert_that(exception_raised)

    def test_should_raise_error_when_function_not_called_with_expected_arguments_but_in_many_other_ways(self):

        when(targetpackage).targetfunction(1, 2).then_return('123')

        targetpackage.targetfunction('abc', 123, True)
        targetpackage.targetfunction('spam', 2, 1, 'eggs', False)
        targetpackage.targetfunction('eggs', False)
        targetpackage.targetfunction()

        exception_raised = False
        try:
            verify(targetpackage).targetfunction(1, 2)
        except VerificationError as error:
            exception_raised = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.targetfunction(1, 2) << at least once >>
 but was: call targetpackage.targetfunction('abc', 123, True)
          call targetpackage.targetfunction('spam', 2, 1, 'eggs', False)
          call targetpackage.targetfunction('eggs', False)
          call targetpackage.targetfunction()
"""))

        assert_that(exception_raised)

    def test_should_verify_a_call_to_a_object_with_multiple_arguments(self):

        test_object = targetpackage.TheClass()

        when(test_object).some_method(1, 2).then_return('123')

        test_object.some_method(1, 2)

        verify(test_object).some_method(1, 2)

    def test_should_verify_a_simple_call_using_a_keyword_argument(self):

        when(targetpackage).targetfunction(keyword_argument='foobar').then_return('123')

        targetpackage.targetfunction(keyword_argument='foobar')

        verify(targetpackage).targetfunction(keyword_argument='foobar')

    def test_should_raise_error_when_function_patched_and_not_called_with_expected_keyword_argument(self):

        when(targetpackage).targetfunction(test=1).then_return('123')

        targetpackage.targetfunction(test=2)

        exception_raised = False
        try:
            verify(targetpackage).targetfunction(test=1)
        except VerificationError as error:
            exception_raised = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.targetfunction(test=1) << at least once >>
 but was: call targetpackage.targetfunction(test=2)
"""))

        assert_that(exception_raised)


class AnyArgumentsVerificationTests(UnitTests):

    def test_should_verify_a_simple_call_with_any_arguments(self):

        when(targetpackage).targetfunction(1).then_return('123')

        targetpackage.targetfunction(1)

        verify(targetpackage).targetfunction(ANY_ARGUMENTS)

    def test_should_raise_exception_when_trying_to_use_any_arguments_with_(self):

        when(targetpackage).targetfunction(1).then_return('123')

        targetpackage.targetfunction(1)

        exception_raised = False

        try:
            verify(targetpackage).targetfunction(ANY_ARGUMENTS, 123)

        except InvalidUseOfAnyArgumentsError as error:
            exception_raised = True
            self.assertEqual(str(error), """Do not use ANY_ARGUMENTS together with other arguments!
Use ANY_ARGUMENT as a wildcard for single arguments.""")

        assert_that(exception_raised)

    def test_should_raise_exception_when_any_arguments_in_arguments_but_not_first(self):

        when(targetpackage).targetfunction(1).then_return('123')

        targetpackage.targetfunction(1)

        exception_raised = False

        try:
            verify(targetpackage).targetfunction(1, 2, 3, ANY_ARGUMENTS)

        except InvalidUseOfAnyArgumentsError as error:
            exception_raised = True
            self.assertEqual(str(error), """Do not use ANY_ARGUMENTS together with other arguments!
Use ANY_ARGUMENT as a wildcard for single arguments.""")

        assert_that(exception_raised)


class MockVerificationTests(UnitTests):

    def test_should_verify_a_call_to_a_field_of_a_mock(self):

        test_object = Mock(targetpackage.TheClass())

        when(test_object).some_method(1).then_return(0)

        assert_that(test_object.some_method(1), equal_to(0))

        verify(test_object).some_method(1)

    def test_should_verify_a_call_to_a_field_of_a_mock_with_any_argument(self):

        test_object = Mock(targetpackage.TheClass())

        when(test_object).some_method(1).then_return(0)

        assert_that(test_object.some_method(1), equal_to(0))

        verify(test_object).some_method(ANY_ARGUMENT)

    def test_should_verify_a_call_to_a_field_of_a_mock_with_some_arguments_and_any_argument(self):

        test_object = Mock(targetpackage.TheClass())

        when(test_object).some_method(ANY_ARGUMENTS).then_return(0)

        assert_that(test_object.some_method(1, 2, 3), equal_to(0))

        verify(test_object).some_method(1, ANY_ARGUMENT, 3)

    def test_should_verify_a_call_to_a_field_of_a_mock_with_any_arguments(self):

        test_object = Mock(targetpackage.TheClass())

        when(test_object).some_method(ANY_ARGUMENTS).then_return(0)

        assert_that(test_object.some_method(1, 2, 3), equal_to(0))

        verify(test_object).some_method(ANY_ARGUMENTS)


class NativeMockVerificationTests(UnitTests):

    def test_should_verify_a_call_to_a_field_of_a_mock_without_any_arguments(self):

        test_object = Mock(targetpackage.TheClass())

        test_object.some_method()

        verify(test_object).some_method()

    def test_should_verify_a_call_to_a_field_of_a_mock_with_arguments(self):

        test_object = Mock(targetpackage.TheClass())

        test_object.some_method(1, 2, 3)

        verify(test_object).some_method(1, 2, 3)

    def test_should_verify_a_call_to_a_field_of_a_mock_with_arguments_and_keyword_arguments(self):

        test_object = Mock(targetpackage.TheClass())

        test_object.some_method(1, 2, 3, hello='world')

        verify(test_object).some_method(1, 2, 3, hello='world')

    def test_should_verify_never_called_a_field_of_a_mock_without_any_arguments(self):

        test_object = Mock(targetpackage.TheClass())

        test_object.some_method(1, 2, 3)

        verify(test_object, NEVER).some_method()

    def test_should_raise_exception_when_called_a_field_of_a_mock_without_any_arguments(self):

        test_object = Mock(targetpackage.TheClass())

        test_object.some_method()

        exception_raised = False
        try:
            verify(test_object, NEVER).some_method()
        except VerificationError as error:
            exception_raised = True
            self.assertEqual(str(error), """
Expected: call mock.Mock.some_method() << should never be called >>
""")

        assert_that(exception_raised)

    def test_should_raise_exception_when_called_a_field_of_a_mock_with_arguments(self):

        test_object = Mock(targetpackage.TheClass())

        test_object.some_method(1, 2, 3)

        exception_raised = False
        try:
            verify(test_object, NEVER).some_method(1, 2, 3)
        except VerificationError as error:
            exception_raised = True
            self.assertEqual(str(error), """
Expected: call mock.Mock.some_method(1, 2, 3) << should never be called >>
""")

        assert_that(exception_raised)

    def test_should_raise_exception_when_called_a_field_of_a_mock_with_keyword_arguments(self):

        test_object = Mock(targetpackage.TheClass())

        test_object.some_method(1, 2, 3, hello='world')

        exception_raised = False
        try:
            verify(test_object, NEVER).some_method(1, 2, 3, hello='world')
        except VerificationError as error:
            exception_raised = True
            self.assertEqual(
                str(error), """
Expected: call mock.Mock.some_method(1, 2, 3, hello='world') << should never be called >>
""")

        assert_that(exception_raised)

    def test_should_raise_exception_when_trying_to_use_matcher_in_native_verification(self):

        test_object = Mock(targetpackage.TheClass())

        test_object.some_method(1, 2, 3, hello='world')

        exception_raised = False
        try:
            verify(test_object).some_method(ANY_ARGUMENT, 2, 3, hello='world')
        except FoundMatcherInNativeVerificationError as error:
            exception_raised = True
            self.assertEqual(
                str(error), """
You were trying to verify mock.Mock.some_method(<< ANY_ARGUMENT >>, 2, 3, hello='world')
fluentmock.verify will call Mock.assert_called_with for verification
when the Mock has not been configured using fluentmock.when
Therefore it is not possible to use matchers when verifying
a Mock without configuring it with fluentmock.when,
because Mock.assert_called_with does not support matchers.
Please configure your mock in order to be able to use a matcher.
""")

        assert_that(exception_raised)

    def test_should_raise_exception_when_trying_to_use_matcher_as_second_argument_in_native_verification(self):

        test_object = Mock(targetpackage.TheClass())

        test_object.some_method(1, 2, 3, hello='world')

        exception_raised = False
        try:
            verify(test_object).some_method(1, ANY_ARGUMENT, 3, hello='world')
        except FoundMatcherInNativeVerificationError as error:
            exception_raised = True
            self.assertEqual(
                str(error), """
You were trying to verify mock.Mock.some_method(1, << ANY_ARGUMENT >>, 3, hello='world')
fluentmock.verify will call Mock.assert_called_with for verification
when the Mock has not been configured using fluentmock.when
Therefore it is not possible to use matchers when verifying
a Mock without configuring it with fluentmock.when,
because Mock.assert_called_with does not support matchers.
Please configure your mock in order to be able to use a matcher.
""")

        assert_that(exception_raised)

    def test_should_raise_exception_when_trying_to_use_matcher_as_keyword_argument_in_native_verification(self):

        test_object = Mock(targetpackage.TheClass())

        test_object.some_method(1, 2, 3, hello='world')

        exception_raised = False
        try:
            verify(test_object).some_method(1, 2, 3, hello=ANY_ARGUMENT)
        except FoundMatcherInNativeVerificationError as error:
            exception_raised = True
            self.assertEqual(
                str(error), """
You were trying to verify mock.Mock.some_method(1, 2, 3, hello=<< ANY_ARGUMENT >>)
fluentmock.verify will call Mock.assert_called_with for verification
when the Mock has not been configured using fluentmock.when
Therefore it is not possible to use matchers when verifying
a Mock without configuring it with fluentmock.when,
because Mock.assert_called_with does not support matchers.
Please configure your mock in order to be able to use a matcher.
""")

        assert_that(exception_raised)

    def test_should_raise_exception_when_trying_to_use_matcher_as_second_keyword_argument_in_native_verification(self):

        test_object = Mock(targetpackage.TheClass())

        test_object.some_method(1, 2, 3, hello='world')

        exception_raised = False
        try:
            verify(test_object).some_method(1, 2, 3, hello='world', world=ANY_ARGUMENT)
        except FoundMatcherInNativeVerificationError as error:
            exception_raised = True
            self.assertTrue(str(error).startswith("""\nYou were trying to verify mock.Mock.some_method(1, 2, 3, """))

        assert_that(exception_raised)


class CouldNotVerifyCallTests(UnitTests):

    def test_should_raise_error_when_two_functions_patched_and_only_one_called(self):

        when(targetpackage).targetfunction().then_return('123')
        when(targetpackage).patch_test_1().then_return('123')

        targetpackage.targetfunction()

        exception_raised = False

        verify(targetpackage).targetfunction()

        try:
            verify(targetpackage).patch_test_1()
        except VerificationError as error:
            exception_raised = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.patch_test_1() << at least once >>
"""))

        assert_that(exception_raised)

    def test_should_show_error_message_including_keyword_arguments_when_two_functions_patched_and_only_one_called(self):

        when(targetpackage).targetfunction().then_return('123')
        when(targetpackage).patch_test_1().then_return('123')

        targetpackage.targetfunction()

        exception_raised = False

        verify(targetpackage).targetfunction()

        try:
            verify(targetpackage).patch_test_1(1, 2, 3, hello='world')
        except VerificationError as error:
            exception_raised = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.patch_test_1(1, 2, 3, hello='world') << at least once >>
"""))

        assert_that(exception_raised)

    def test_should_raise_error_and_list_the_expected_arguments_when_function_not_called(self):

        when(targetpackage).targetfunction().then_return('123')
        when(targetpackage).patch_test_1().then_return('123')

        targetpackage.targetfunction()

        exception_raised = False

        verify(targetpackage).targetfunction()

        try:
            verify(targetpackage).patch_test_1(1, 2, 3)
        except VerificationError as error:
            exception_raised = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.patch_test_1(1, 2, 3) << at least once >>
"""))

        assert_that(exception_raised)


class VerifiyNeverTests(UnitTests):

    def test_should_verify_that_function_has_not_been_called_when_function_has_been_called_with_other_arguments(self):

        when(targetpackage).targetfunction().then_return('123')

        targetpackage.targetfunction(1)

        verify(targetpackage, NEVER).targetfunction()

    def test_should_verify_that_function_has_not_been_called(self):

        when(targetpackage).targetfunction().then_return('123')

        verify(targetpackage, NEVER).targetfunction()

    def test_should_raise_error_when_function_called_but_it_should_not_have_been_called(self):

        when(targetpackage).targetfunction(1, 2, 3, test=1).then_return('123')

        targetpackage.targetfunction(1, 2, 3, test=1)

        exception_raised = False
        try:
            verify(targetpackage, NEVER).targetfunction(1, 2, 3, test=1)
        except VerificationError as error:
            exception_raised = True
            error_message = """
Expected: call targetpackage.targetfunction(1, 2, 3, test=1) << should never be called >>
"""
            assert_that(str(error), equal_to(error_message))

        assert_that(exception_raised)


class NoCallsStoredTests(UnitTests):

    def test_should_not_verify_a_call_when_no_function_has_been_called(self):

        when(targetpackage).targetfunction().then_return('123')

        exception_raised = False

        try:
            verify(targetpackage).targetfunction(1, 2, 3, hello='foobar')
        except VerificationError as error:
            exception_raised = True
            self.assertEqual("""
Expected: call targetpackage.targetfunction(1, 2, 3, hello='foobar') << at least once >>
  Reason: No patched function has been called.
""", str(error))

        assert_that(exception_raised)

    def test_should_not_verify_a_simple_call_when_no_function_has_been_called(self):

        when(targetpackage).targetfunction().then_return('123')

        exception_raised = False

        try:
            verify(targetpackage).targetfunction()
        except VerificationError as error:
            exception_raised = True
            self.assertEqual("""
Expected: call targetpackage.targetfunction() << at least once >>
  Reason: No patched function has been called.
""", str(error))

        assert_that(exception_raised)

    def test_should_raise_error_with_a_detailed_message_when_function_patched_and_not_called(self):

        when(targetpackage).targetfunction().then_return('123')

        exception_raised = False
        try:
            verify(targetpackage).targetfunction()
        except VerificationError as error:
            exception_raised = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.targetfunction() << at least once >>
  Reason: No patched function has been called.
"""))
        assert_that(exception_raised)


class VerifyAnyArgumentTests(UnitTests):

    def test_should_verify_any_argument(self):

        when(targetpackage).targetfunction(ANY_ARGUMENT).then_return(1)

        targetpackage.targetfunction(2)

        verify(targetpackage).targetfunction(ANY_ARGUMENT)

    def test_should_verify_any_argument_twice(self):

        when(targetpackage).targetfunction(ANY_ARGUMENTS).then_return(1)

        targetpackage.targetfunction(2, 'abc')

        verify(targetpackage).targetfunction(ANY_ARGUMENT, ANY_ARGUMENT)

    def test_should_raise_error_with_a_detailed_message_when_any_argument_does_not_match(self):

        when(targetpackage).targetfunction(ANY_ARGUMENTS).then_return('123')

        targetpackage.targetfunction(1, 2, 3)

        exception_raised = False
        try:
            verify(targetpackage).targetfunction(1, ANY_ARGUMENT, 'c')
        except VerificationError as error:
            exception_raised = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.targetfunction(1, << ANY_ARGUMENT >>, 'c') << at least once >>
 but was: call targetpackage.targetfunction(1, 2, 3)
"""))
        assert_that(exception_raised)


class TimesVerificationTests(UnitTests):

    def test_should_verify_that_target_has_been_called_exactly_once(self):

        when(targetpackage).targetfunction(ANY_ARGUMENTS).then_return(123)

        targetpackage.targetfunction("abc")

        verify(targetpackage, times=1).targetfunction("abc")

    def test_should_raise_exception_when_times_is_not_instance_of_fluentmatcher_or_integer(self):

        when(targetpackage).targetfunction(ANY_ARGUMENTS).then_return(123)

        targetpackage.targetfunction("abc")

        exception_raised = False
        try:
            verify(targetpackage, times='123').targetfunction('abc')
        except ValueError as error:
            exception_raised = True
            assert_that(str(error), equal_to('Argument times has to be a instance of FluentMatcher'))

        assert_that(exception_raised)

    def test_should_raise_exception_when_times_is_two_but_target_called_once(self):

        when(targetpackage).targetfunction(ANY_ARGUMENTS).then_return(123)

        targetpackage.targetfunction("abc")

        exception_raised = False
        try:
            verify(targetpackage, times=2).targetfunction('abc')
        except VerificationError as error:
            exception_raised = True
            assert_that(str(error), equal_to(
                """
Expected: call targetpackage.targetfunction('abc') << should be called exactly 2 times >>
"""))

        assert_that(exception_raised)

    def test_should_verify_that_target_has_been_called_exactly_three_times(self):

        when(targetpackage).targetfunction(ANY_ARGUMENTS).then_return(123)

        targetpackage.targetfunction("abc")
        targetpackage.targetfunction("abc")
        targetpackage.targetfunction("abc")
        targetpackage.targetfunction(1)
        targetpackage.targetfunction(1)
        targetpackage.targetfunction(1, 2, 3)

        verify(targetpackage, times=3).targetfunction("abc")
        verify(targetpackage, times=2).targetfunction(1)
        verify(targetpackage, times=1).targetfunction(1, 2, 3)

    def test_should_verify_that_mock_has_been_called_exactly_once(self):

        test_object = Mock(targetpackage.TheClass())

        when(test_object).some_method(1).then_return(0)

        assert_that(test_object.some_method(1), equal_to(0))

        verify(test_object, times=1).some_method(1)

    def test_should_raise_exception_when_called_a_field_of_a_mock_once_but_twice_expected(self):

        test_object = Mock(targetpackage.TheClass())

        test_object.some_method(1, 2, 3)

        exception_raised = False
        try:
            verify(test_object, times=2).some_method(1, 2, 3)
        except VerificationError as error:
            exception_raised = True
            self.assertEqual(str(error), """
Expected: call mock.Mock.some_method(1, 2, 3) << should be called exactly 2 times >>
""")

        assert_that(exception_raised)

    def test_should_raise_exception_when_called_once_but_expected_twice_with_any_arguments(self):

        when(targetpackage).targetfunction(ANY_ARGUMENTS).then_return(123)

        targetpackage.targetfunction("abc")

        exception_raised = False
        try:
            verify(targetpackage, times=2).targetfunction(ANY_ARGUMENTS)
        except VerificationError as error:
            exception_raised = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.targetfunction(<< ANY_ARGUMENTS >>) << should be called exactly 2 times >>
"""))

        assert_that(exception_raised)
