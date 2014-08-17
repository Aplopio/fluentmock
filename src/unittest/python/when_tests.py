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
from mock import Mock

from fluentmock import ANY_VALUE, ANY_VALUES, FluentAnswer, FluentMockConfigurator, UnitTests, when
from fluentmock.exceptions import InvalidAttributeError, InvalidUseOfAnyValuesError

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

        assert_that(exception_raised)

    def test_should_patch_away_method_of_mock(self):

        test_object = Mock(targetpackage.TheClass())

        when(test_object).some_method(1).then_return(0)

        assert_that(test_object.some_method(1), equal_to(0))

    def test_should_patch_away_method_of_subpackage(self):

        when(targetpackage.subpackage).subtargetfunction(0).then_return(0)

        assert_that(targetpackage.subpackage.subtargetfunction(0), equal_to(0))

    def test_should_return_none_when_configured_for_keyword_argument_but_not_called_with_it(self):

        when(targetpackage).targetfunction(keyword_argument='abc').then_return('foobar')

        assert_that(targetpackage.targetfunction(), equal_to(None))

    def test_should_return_configured_answer_when_keyword_argument_given(self):

        when(targetpackage).targetfunction(keyword_argument='abc').then_return('foobar')

        assert_that(targetpackage.targetfunction(keyword_argument='abc'), equal_to('foobar'))

    def test_should_remove_predefined_answer_when_new_answer_given(self):

        when(targetpackage).targetfunction(1).then_return('Nope!')
        when(targetpackage).targetfunction(1).then_return('Yes.')

        assert_that(targetpackage.targetfunction(1), equal_to('Yes.'))

    def test_should_remove_predefined_answer_when_multiple_new_answers_given(self):

        when(targetpackage).targetfunction(1).then_return('Nope!')
        when(targetpackage).targetfunction(1).then_return('Yes.').then_return('Maybe!').then_return('No.')

        assert_that(targetpackage.targetfunction(1), equal_to('Yes.'))
        assert_that(targetpackage.targetfunction(1), equal_to('Maybe!'))
        assert_that(targetpackage.targetfunction(1), equal_to('No.'))

    def test_should_remove_predefined_answers_when_multiple_new_answers_given(self):

        when(targetpackage).targetfunction(1).then_return('Nope!').then_return('Never.').then_return('Ever.')
        when(targetpackage).targetfunction(1).then_return('Yes.').then_return('Maybe!').then_return('No.')

        assert_that(targetpackage.targetfunction(1), equal_to('Yes.'))
        assert_that(targetpackage.targetfunction(1), equal_to('Maybe!'))
        assert_that(targetpackage.targetfunction(1), equal_to('No.'))
        assert_that(targetpackage.targetfunction(1), equal_to('No.'))
        assert_that(targetpackage.targetfunction(1), equal_to('No.'))


class AnyArgumentsTest(UnitTests):

    def test_should_always_return_the_same_answer_for_any_argument(self):

        when(targetpackage).targetfunction(ANY_VALUES).then_return('foobar')

        assert_that(targetpackage.targetfunction(0), equal_to('foobar'))
        assert_that(targetpackage.targetfunction(1, 2, 3), equal_to('foobar'))
        assert_that(targetpackage.targetfunction(), equal_to('foobar'))
        assert_that(targetpackage.targetfunction('hello', 1), equal_to('foobar'))

    def test_should_raise_exception_when_configured_to_raise_exception(self):

        when(targetpackage).targetfunction(ANY_VALUES).then_raise(Exception('foobar'))

        exception_raised = False
        try:
            targetpackage.targetfunction()
        except Exception as exception:
            exception_raised = True
            assert_that(str(exception), equal_to('foobar'))

        assert_that(exception_raised)

    def test_should_raise_exception_when_trying_to_configure_mock_with_any_arguments_with_other_arguments(self):

        exception_raised = False
        try:
            when(targetpackage).targetfunction(ANY_VALUES, 1, 2, 3).then_raise(Exception('foobar'))
        except InvalidUseOfAnyValuesError as exception:
            exception_raised = True
            assert_that(str(exception), equal_to("""Do not use ANY_VALUES together with other arguments!
Use ANY_VALUE as a wildcard for single arguments."""))

        assert_that(exception_raised)

    def test_should_raise_exception_when_trying_to_configure_mock_with_any_arguments_as_second_argument(self):

        exception_raised = False
        try:
            when(targetpackage).targetfunction(1, ANY_VALUES, 2, 3).then_raise(Exception('foobar'))
        except InvalidUseOfAnyValuesError as exception:
            exception_raised = True
            assert_that(str(exception), equal_to("""Do not use ANY_VALUES together with other arguments!
Use ANY_VALUE as a wildcard for single arguments."""))

        assert_that(exception_raised)

    def test_should_return_configured_answer_when_addressing_target_using_string(self):

        when('targetpackage').targetfunction(ANY_VALUES).then_return('foobar')

        assert_that(targetpackage.targetfunction(keyword_argument='abc'), equal_to('foobar'))


class AnyArgumentTests(UnitTests):

    def test_should_match_argument_when_using_any_argument(self):

        when(targetpackage.subpackage).subtargetfunction(ANY_VALUE).then_return('specific')

        assert_that(targetpackage.subpackage.subtargetfunction(1), equal_to('specific'))
        assert_that(targetpackage.subpackage.subtargetfunction(2), equal_to('specific'))
        assert_that(targetpackage.subpackage.subtargetfunction(3), equal_to('specific'))

    def test_should_match_number_of_arguments_when_using_any_argument(self):

        when(targetpackage.subpackage).subtargetfunction(ANY_VALUE).then_return('specific')

        assert_that(targetpackage.subpackage.subtargetfunction(0, 1), equal_to(None))

    def test_should_match_number_of_keyword_arguments_when_using_any_argument(self):

        when(targetpackage.subpackage).subtargetfunction(ANY_VALUE).then_return('specific')

        assert_that(targetpackage.subpackage.subtargetfunction(0, hello='world'), equal_to(None))

    def test_should_match_second_argument_when_using_any_argument_on_second_argument(self):

        when(targetpackage.subpackage).subtargetfunction(1, ANY_VALUE).then_return('specific')

        assert_that(targetpackage.subpackage.subtargetfunction(1, 2), equal_to('specific'))

    def test_should_not_match_when_using_any_argument_on_second_argument_and_first_argument_different(self):

        when(targetpackage.subpackage).subtargetfunction(1, ANY_VALUE).then_return('specific')

        assert_that(targetpackage.subpackage.subtargetfunction(0, 2), equal_to(None))

    def test_should_match_when_using_any_argument_on_second_argument_and_third_argument_is_keyword_argument(self):

        when(targetpackage.subpackage).subtargetfunction(1, ANY_VALUE, foo='spam').then_return('specific')

        assert_that(targetpackage.subpackage.subtargetfunction(1, 2, foo='spam'), equal_to('specific'))

    def test_should_not_match_when_using_any_argument_on_second_argument_and_keyword_argument_does_not_match(self):

        when(targetpackage.subpackage).subtargetfunction(1, ANY_VALUE, foo='spam').then_return('specific')

        assert_that(targetpackage.subpackage.subtargetfunction(1, 2, foo='eggs'), equal_to(None))

    def test_should_not_match_when_using_any_argument_on_second_argument_and_keyword_arguments_do_not_match(self):

        when(targetpackage.subpackage).subtargetfunction(1, ANY_VALUE, foo='bar', spam='egg').then_return('specific')

        assert_that(targetpackage.subpackage.subtargetfunction(1, 2, foo='bar', spam='blabla'), equal_to(None))

    def test_should_match_when_using_any_argument_on_second_argument_and_two_keyword_arguments_match(self):

        when(targetpackage.subpackage).subtargetfunction(1, ANY_VALUE, foo='bar', spam='egg').then_return('specific')

        assert_that(targetpackage.subpackage.subtargetfunction(1, 2, foo='bar', spam='egg'), equal_to('specific'))

    def test_should_match_when_using_any_argument_on_second_argument_and_three_keyword_arguments_match(self):

        when(targetpackage.subpackage).subtargetfunction(1, ANY_VALUE, a='1', b='2', c='3').then_return('specific')

        assert_that(targetpackage.subpackage.subtargetfunction(1, 2, a='1', b='2', c='3'), equal_to('specific'))

    def test_should_match_when_using_any_argument_on_keyword_argument(self):

        when(targetpackage.subpackage).subtargetfunction(1, a='1', b=ANY_VALUE, c='3').then_return('specific')

        assert_that(targetpackage.subpackage.subtargetfunction(1, a='1', b='hello world', c='3'), equal_to('specific'))

    def test_should_not_match_when_using_any_argument_but_equal_number_of_keyword_arguments(self):

        when(targetpackage.subpackage).subtargetfunction(1, ANY_VALUE, foo='bar', spam='egg').then_return('specific')

        assert_that(targetpackage.subpackage.subtargetfunction(1, 2, foo='bar', blam='blabla'), equal_to(None))

    def test_should_not_match_when_using_any_argument_but_equal_number_of_keyword_arguments_but_not_equal_keys(self):

        when(targetpackage.subpackage).subtargetfunction(1, ANY_VALUE, foo='bar', spam='egg').then_return('specific')

        assert_that(targetpackage.subpackage.subtargetfunction(1, 2, zap='bran', spam='blabla'), equal_to(None))
