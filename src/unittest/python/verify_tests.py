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
from fluentmock import UnitTests, FluentMockException, when, verify

import targetpackage


class VerifyTests(UnitTests):

    def test_should_verify_a_simple_call(self):

        when(targetpackage).targetfunction().then_return('123')

        targetpackage.targetfunction()

        verify(targetpackage).targetfunction()

    def test_should_raise_exception_when_target_does_not_have_attribute(self):

        when(targetpackage).targetfunction().then_return('123')

        targetpackage.targetfunction()

        raised_exception = False
        try:
            verify(targetpackage).spameggs
        except FluentMockException as exception:
            raised_exception = True
            self.assertEqual('The target "targetpackage" has no attribute called "spameggs".', str(exception))

        assert_that(raised_exception, "Did not raise exception even though target does not have attribute.")

    def test_should_not_verify_a_simple_call(self):

        when(targetpackage).targetfunction().then_return('123')

        raised_error = False

        try:
            verify(targetpackage).targetfunction()
        except AssertionError as error:
            raised_error = True
            self.assertEqual("""
Expected: call targetpackage.targetfunction()
     Got: no patched function has been called.
""", str(error))

        assert_that(raised_error, "Did not raise assertion error even though function has never been called.")

    def test_should_raise_error_when_two_functions_patched_and_only_one_called(self):

        when(targetpackage).targetfunction().then_return('123')
        when(targetpackage).patch_test_1().then_return('123')

        targetpackage.targetfunction()

        raised_error = False

        verify(targetpackage).targetfunction()

        try:
            verify(targetpackage).patch_test_1()
        except AssertionError as error:
            raised_error = True
            self.assertEqual('Could not verify targetpackage.patch_test_1()', str(error))

        assert_that(raised_error, "Did not raise assertion error even though function has never been called.")

    def test_should_raise_error_with_a_detailed_message_when_function_patched_and_not_called(self):

        when(targetpackage).targetfunction().then_return('123')

        raised_error = False
        try:
            verify(targetpackage).targetfunction()
        except AssertionError as error:
            raised_error = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.targetfunction()
     Got: no patched function has been called.
"""))
        assert_that(raised_error, "Did not raise error even though function has never been called.")

    def test_should_verify_a_simple_call_with_a_argument(self):

        when(targetpackage).targetfunction(1).then_return('123')

        targetpackage.targetfunction(1)

        verify(targetpackage).targetfunction(1)

    def test_should_raise_error_when_function_patched_and_not_called_with_expected_argument(self):

        when(targetpackage).targetfunction(1).then_return('123')

        targetpackage.targetfunction(2)

        raised_error = False
        try:
            verify(targetpackage).targetfunction(1)
        except AssertionError as error:
            raised_error = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.targetfunction(1)
 but was: call targetpackage.targetfunction(2)
"""))

        assert_that(raised_error, "Did not raise error even though function has been called with other arguments.")

    def test_should_verify_a_call_with_multiple_arguments(self):

        when(targetpackage).targetfunction(1, 2).then_return('123')

        targetpackage.targetfunction(1, 2)

        verify(targetpackage).targetfunction(1, 2)

    def test_should_raise_error_when_function_patched_and_not_called_with_expected_arguments(self):

        when(targetpackage).targetfunction(1, 2).then_return('123')

        targetpackage.targetfunction(2, 1)

        raised_error = False
        try:
            verify(targetpackage).targetfunction(1, 2)
        except AssertionError as error:
            raised_error = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.targetfunction(1, 2)
 but was: call targetpackage.targetfunction(2, 1)
"""))

        assert_that(raised_error, "Did not raise error even though function has been called with other arguments.")

    def test_should_raise_error_when_function_not_called_with_expected_arguments_but_in_other_ways(self):

        when(targetpackage).targetfunction(1, 2).then_return('123')

        targetpackage.targetfunction('abc', 123, True)
        targetpackage.targetfunction('spam', 2, 1, 'eggs', False)

        raised_error = False
        try:
            verify(targetpackage).targetfunction(1, 2)
        except AssertionError as error:
            raised_error = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.targetfunction(1, 2)
 but was: call targetpackage.targetfunction('abc', 123, True)
          call targetpackage.targetfunction('spam', 2, 1, 'eggs', False)
"""))

        assert_that(raised_error, "Did not raise error even though function has been called with other arguments.")

    def test_should_raise_error_when_function_not_called_with_expected_arguments_but_in_many_other_ways(self):

        when(targetpackage).targetfunction(1, 2).then_return('123')

        targetpackage.targetfunction('abc', 123, True)
        targetpackage.targetfunction('spam', 2, 1, 'eggs', False)
        targetpackage.targetfunction('eggs', False)
        targetpackage.targetfunction()

        raised_error = False
        try:
            verify(targetpackage).targetfunction(1, 2)
        except AssertionError as error:
            raised_error = True
            assert_that(str(error), equal_to("""
Expected: call targetpackage.targetfunction(1, 2)
 but was: call targetpackage.targetfunction('abc', 123, True)
          call targetpackage.targetfunction('spam', 2, 1, 'eggs', False)
          call targetpackage.targetfunction('eggs', False)
          call targetpackage.targetfunction()
"""))

        assert_that(raised_error, "Did not raise error even though function has been called with other arguments.")

    def test_should_verify_a_call_to_a_object_with_multiple_arguments(self):

        test_object = targetpackage.TheClass()

        when(test_object).some_method(1, 2).then_return('123')

        test_object.some_method(1, 2)

        verify(test_object).some_method(1, 2)
