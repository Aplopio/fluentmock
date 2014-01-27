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

from hamcrest import assert_that, equal_to, instance_of
from fluentmock import ANY_ARGUMENTS, FluentAnswer, FluentMockConfigurator, InvalidAttributeError, UnitTests, when
from mock import Mock

import targetpackage
import targetpackage.subpackage


class WhenTests(UnitTests):

    def test_should_return_wrapper_when_patching_module(self):

        actual = when(targetpackage).targetfunction

        assert_that(actual, instance_of(FluentMockConfigurator))

    def test_should_return_answer_when_calling_patched_function(self):

        actual = when(targetpackage).targetfunction()

        assert_that(actual, instance_of(FluentAnswer))

    def test_should_return_None_when_no_answer_is_configured(self):

        when(targetpackage).targetfunction()

        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(None))

    def test_should_return_zero_when_answer_zero_is_given(self):

        when(targetpackage).targetfunction().then_return(0)

        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(0))

    def test_should_return_zero_again_when_answer_zero_is_given(self):

        when(targetpackage).targetfunction().then_return(0)

        targetpackage.targetfunction()
        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(0))

    def test_should_return_one_as_first_answer_when_two_answers_are_configured(self):

        when(targetpackage).targetfunction().then_return(1).then_return(2)

        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(1))

    def test_should_return_wrapper_when_call_definition(self):

        actual = when(targetpackage).targetfunction().then_return(1)

        assert_that(actual, instance_of(FluentAnswer))

    def test_should_return_two_as_second_answer_when_two_answers_are_configured(self):

        when(targetpackage).targetfunction().then_return(1).then_return(2)

        targetpackage.targetfunction()
        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(2))

    def test_should_return_three_as_third_answer_when_three_answers_are_configured(self):

        when(targetpackage).targetfunction().then_return(1).then_return(2).then_return(3)

        targetpackage.targetfunction()
        targetpackage.targetfunction()
        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(3))

    def test_should_return_four_as_fourth_answer_when_four_answers_are_configured(self):

        when(targetpackage).targetfunction().then_return(1).then_return(2).then_return(3).then_return(4)

        targetpackage.targetfunction()
        targetpackage.targetfunction()
        targetpackage.targetfunction()
        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(4))

    def test_should_return_four_as_fifth_answer_when_four_answers_are_configured(self):

        when(targetpackage).targetfunction().then_return(1).then_return(2).then_return(3).then_return(4)

        targetpackage.targetfunction()
        targetpackage.targetfunction()
        targetpackage.targetfunction()
        targetpackage.targetfunction()
        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(4))

    def test_should_return_specific_value_when_argument_fits(self):

        when(targetpackage).targetfunction(1).then_return(1)

        assert_that(targetpackage.targetfunction(1), equal_to(1))
        assert_that(targetpackage.targetfunction(0), equal_to(None))

    def test_should_return_specific_value_when_argument_fits_and_several_configurations_are_given(self):

        when(targetpackage).targetfunction(1).then_return(1)
        when(targetpackage).targetfunction(2).then_return(2)
        when(targetpackage).targetfunction(3).then_return(3)

        assert_that(targetpackage.targetfunction(3), equal_to(3))
        assert_that(targetpackage.targetfunction(2), equal_to(2))
        assert_that(targetpackage.targetfunction(1), equal_to(1))
        assert_that(targetpackage.targetfunction(0), equal_to(None))

    def test_should_return_specific_value_when_arguments_fit(self):

        when(targetpackage).targetfunction(1, 'spam').then_return(1)

        assert_that(targetpackage.targetfunction(1, 'spam'), equal_to(1))
        assert_that(targetpackage.targetfunction(0), equal_to(None))

    def test_should_return_specific_values_when_arguments_fit(self):

        when(targetpackage).targetfunction(2).then_return(2)
        when(targetpackage).targetfunction(1, 'spam').then_return(1)
        when(targetpackage).targetfunction(3, 'foo', True).then_return('bar')

        assert_that(targetpackage.targetfunction(1, 'spam'), equal_to(1))
        assert_that(targetpackage.targetfunction(3, 'foo', True), equal_to('bar'))
        assert_that(targetpackage.targetfunction(2), equal_to(2))
        assert_that(targetpackage.targetfunction(0), equal_to(None))

    def test_should_patch_away_method_of_object(self):

        test_object = targetpackage.TheClass()

        when(test_object).some_method(1).then_return(0)

        assert_that(test_object.some_method(1), equal_to(0))

    def test_should_give_useful_feedback_if_target_does_not_have_attribute(self):

        exception_raised = False
        try:
            when(targetpackage).invalid_function(1)
        except InvalidAttributeError as error:
            exception_raised = True
            self.assertEqual('The target "targetpackage" has no attribute called "invalid_function".', str(error))

        self.assertTrue(exception_raised, "Did not raise exception when trying to patch away an invalid function")

    def test_should_patch_away_method_of_mock(self):

        test_object = Mock(targetpackage.TheClass())

        when(test_object).some_method(1).then_return(0)

        assert_that(test_object.some_method(1), equal_to(0))

    def test_should_patch_away_method_of_subpackage(self):

        when(targetpackage.subpackage).subtargetfunction(0).then_return(0)

        assert_that(targetpackage.subpackage.subtargetfunction(0), equal_to(0))

    def test_should_always_return_the_same_answer_for_any_argument(self):

        when(targetpackage).targetfunction(ANY_ARGUMENTS).then_return('foobar')

        assert_that(targetpackage.targetfunction(0), equal_to('foobar'))
        assert_that(targetpackage.targetfunction(1, 2, 3), equal_to('foobar'))
        assert_that(targetpackage.targetfunction(), equal_to('foobar'))
        assert_that(targetpackage.targetfunction('hello', 1), equal_to('foobar'))

    def test_should_raise_exception_when_configured_to_raise_exception(self):

        when(targetpackage).targetfunction(ANY_ARGUMENTS).then_raise(Exception('foobar'))

        exception_raised = False
        try:
            targetpackage.targetfunction()
        except Exception as exception:
            exception_raised = True
            assert_that(str(exception), equal_to('foobar'))

        self.assertTrue(exception_raised, 'Exception has not been raised event thow the mock has been configured so.')

    def test_should_return_none_when_configured_for_keyword_argument_but_not_called_with_it(self):

        when(targetpackage).targetfunction(keyword_argument='abc').then_return('foobar')

        assert_that(targetpackage.targetfunction(), equal_to(None))

    def test_should_return_configured_answer_when_keyword_argument_given(self):

        when(targetpackage).targetfunction(keyword_argument='abc').then_return('foobar')

        assert_that(targetpackage.targetfunction(keyword_argument='abc'), equal_to('foobar'))

    def test_should_return_configured_answer_when_addressing_target_using_string(self):

        when('targetpackage').targetfunction(ANY_ARGUMENTS).then_return('foobar')

        assert_that(targetpackage.targetfunction(keyword_argument='abc'), equal_to('foobar'))
