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

from unittest import TestCase

from fluentmock import FluentMockException, MockWrapper, Answer, when, unstub

import targetpackage


class WhenTests(TestCase):

    def test_should_raise_exception_when_target_does_not_have_attribute(self):

        raised_exception = False

        try:
            when(targetpackage).spameggs
        except FluentMockException:
            raised_exception = True

        self.assertTrue(raised_exception, "Did not raise exception when invalid attribute name was given.")

    def test_should_return_wrapper_when_patching_module(self):

        actual = when(targetpackage).targetfunction

        self.assert_is_a_instance_of(actual, MockWrapper)

    def test_should_raise_exception_when_no_answer_configured(self):

        when(targetpackage).targetfunction

        self.assertRaises(FluentMockException, targetpackage.targetfunction)

    def test_should_return_answer_when_calling_patched_function(self):

        actual = when(targetpackage).targetfunction()

        self.assert_is_a_instance_of(actual, Answer)

    def test_should_return_None_when_no_answer_is_configured(self):

        when(targetpackage).targetfunction()

        actual_value = targetpackage.targetfunction()

        self.assertEqual(None, actual_value)

    def test_should_return_zero_when_answer_zero_is_given(self):

        when(targetpackage).targetfunction().then_return(0)

        actual_value = targetpackage.targetfunction()

        self.assertEqual(0, actual_value)

    def test_should_return_zero_again_when_answer_zero_is_given(self):

        when(targetpackage).targetfunction().then_return(0)

        targetpackage.targetfunction()
        actual_value = targetpackage.targetfunction()

        self.assertEqual(0, actual_value)

    def test_should_return_one_as_first_answer_when_two_answers_are_configured(self):

        when(targetpackage).targetfunction().then_return(1).then_return(2)

        actual_value = targetpackage.targetfunction()

        self.assertEqual(1, actual_value)

    def test_should_return_wrapper_when_call_definition(self):

        actual = when(targetpackage).targetfunction().then_return(1)

        self.assert_is_a_instance_of(actual, Answer)

    def test_should_return_two_as_second_answer_when_two_answers_are_configured(self):

        when(targetpackage).targetfunction().then_return(1).then_return(2)

        targetpackage.targetfunction()
        actual_value = targetpackage.targetfunction()

        self.assertEqual(2, actual_value)

    def test_should_return_three_as_third_answer_when_three_answers_are_configured(self):

        when(targetpackage).targetfunction().then_return(1).then_return(2).then_return(3)

        targetpackage.targetfunction()
        targetpackage.targetfunction()
        actual_value = targetpackage.targetfunction()

        self.assertEqual(3, actual_value)

    def test_should_return_four_as_fourth_answer_when_four_answers_are_configured(self):

        when(targetpackage).targetfunction().then_return(1).then_return(2).then_return(3).then_return(4)

        targetpackage.targetfunction()
        targetpackage.targetfunction()
        targetpackage.targetfunction()
        actual_value = targetpackage.targetfunction()

        self.assertEqual(4, actual_value)

    def test_should_return_four_as_fifth_answer_when_four_answers_are_configured(self):

        when(targetpackage).targetfunction().then_return(1).then_return(2).then_return(3).then_return(4)

        targetpackage.targetfunction()
        targetpackage.targetfunction()
        targetpackage.targetfunction()
        targetpackage.targetfunction()
        actual_value = targetpackage.targetfunction()

        self.assertEqual(4, actual_value)

    def assert_is_a_instance_of(self, actual, Class):
        error_message = 'The object "{object}" is not a instance of "{class_name}"'.format(object=str(actual),
                                                                                           class_name=Class.__name__)
        self.assertTrue(isinstance(actual, Class), error_message)


class UnstubTests(TestCase):

    def test_should_unstub_stubbed_function(self):

        when(targetpackage).stub_test_1()

        unstub()

        self.assertEqual('not stubbed 1', targetpackage.stub_test_1())

    def test_should_unstub_multiple_stubbed_function(self):

        when(targetpackage).stub_test_1()
        when(targetpackage).stub_test_2()

        unstub()

        self.assertEqual('not stubbed 1', targetpackage.stub_test_1())
        self.assertEqual('not stubbed 2', targetpackage.stub_test_2())
