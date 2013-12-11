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

from hamcrest import assert_that, equal_to, instance_of
from fluentmock import FluentAnswer, FluentMockException, FluentMockConfigurator, UnitTests, when

import targetpackage


class WhenTests(UnitTests):

    def should_raise_exception_when_target_does_not_have_attribute(self):

        raised_exception = False

        try:
            when(targetpackage).spameggs
        except FluentMockException:
            raised_exception = True

        assert_that(raised_exception, "Did not raise exception when invalid attribute name was given.")

    def should_return_wrapper_when_patching_module(self):

        actual = when(targetpackage).targetfunction

        assert_that(actual, instance_of(FluentMockConfigurator))

    def should_return_answer_when_calling_patched_function(self):

        actual = when(targetpackage).targetfunction()

        assert_that(actual, instance_of(FluentAnswer))

    def should_return_None_when_no_answer_is_configured(self):

        when(targetpackage).targetfunction()

        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(None))

    def should_return_zero_when_answer_zero_is_given(self):

        when(targetpackage).targetfunction().then_return(0)

        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(0))

    def should_return_zero_again_when_answer_zero_is_given(self):

        when(targetpackage).targetfunction().then_return(0)

        targetpackage.targetfunction()
        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(0))

    def should_return_one_as_first_answer_when_two_answers_are_configured(self):

        when(targetpackage).targetfunction().then_return(1).then_return(2)

        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(1))

    def should_return_wrapper_when_call_definition(self):

        actual = when(targetpackage).targetfunction().then_return(1)

        assert_that(actual, instance_of(FluentAnswer))

    def should_return_two_as_second_answer_when_two_answers_are_configured(self):

        when(targetpackage).targetfunction().then_return(1).then_return(2)

        targetpackage.targetfunction()
        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(2))

    def should_return_three_as_third_answer_when_three_answers_are_configured(self):

        when(targetpackage).targetfunction().then_return(1).then_return(2).then_return(3)

        targetpackage.targetfunction()
        targetpackage.targetfunction()
        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(3))

    def should_return_four_as_fourth_answer_when_four_answers_are_configured(self):

        when(targetpackage).targetfunction().then_return(1).then_return(2).then_return(3).then_return(4)

        targetpackage.targetfunction()
        targetpackage.targetfunction()
        targetpackage.targetfunction()
        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(4))

    def should_return_four_as_fifth_answer_when_four_answers_are_configured(self):

        when(targetpackage).targetfunction().then_return(1).then_return(2).then_return(3).then_return(4)

        targetpackage.targetfunction()
        targetpackage.targetfunction()
        targetpackage.targetfunction()
        targetpackage.targetfunction()
        actual_value = targetpackage.targetfunction()

        assert_that(actual_value, equal_to(4))

    def should_return_specific_value_when_argument_fits(self):

        when(targetpackage).targetfunction(1).then_return(1)

        assert_that(targetpackage.targetfunction(1), equal_to(1))
        assert_that(targetpackage.targetfunction(0), equal_to(None))

    def should_return_specific_value_when_argument_fits_and_several_configurations_are_given(self):

        when(targetpackage).targetfunction(1).then_return(1)
        when(targetpackage).targetfunction(2).then_return(2)
        when(targetpackage).targetfunction(3).then_return(3)

        assert_that(targetpackage.targetfunction(3), equal_to(3))
        assert_that(targetpackage.targetfunction(2), equal_to(2))
        assert_that(targetpackage.targetfunction(1), equal_to(1))
        assert_that(targetpackage.targetfunction(0), equal_to(None))

    def should_return_specific_value_when_arguments_fit(self):

        when(targetpackage).targetfunction(1, 'spam').then_return(1)

        assert_that(targetpackage.targetfunction(1, 'spam'), equal_to(1))
        assert_that(targetpackage.targetfunction(0), equal_to(None))

    def should_return_specific_values_when_arguments_fit(self):

        when(targetpackage).targetfunction(2).then_return(2)
        when(targetpackage).targetfunction(1, 'spam').then_return(1)
        when(targetpackage).targetfunction(3, 'foo', True).then_return('bar')

        assert_that(targetpackage.targetfunction(1, 'spam'), equal_to(1))
        assert_that(targetpackage.targetfunction(3, 'foo', True), equal_to('bar'))
        assert_that(targetpackage.targetfunction(2), equal_to(2))
        assert_that(targetpackage.targetfunction(0), equal_to(None))

    def should_stub_away_method_from_object(self):

        test_object = targetpackage.TheClass()

        when(test_object).some_method(1).then_return(0)

        assert_that(test_object.some_method(1), equal_to(0))
