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

__author__ = 'Michael Gruber'
__version__ = '${version}'

from importlib import import_module
from mock import Mock, call, patch
from logging import getLogger
from unittest import TestCase
from types import ModuleType

LOGGER = getLogger(__name__)


MESSAGE_COULD_NOT_VERIFY = 'Could not verify {expected}'
MESSAGE_HAS_BEEN_CALLED_AT_LEAST_ONCE = """{call_entry} should NEVER have been called,
but has been called at least once."""
MESSAGE_INVALID_ATTRIBUTE = 'The target "{target_name}" has no attribute called "{attribute_name}".'
MESSAGE_NO_CALLS = """
Expected: {expected}
 but was: no patched function has been called.
"""
MESSAGE_EXPECTED_BUT_WAS = """
Expected: {expected}
 but was: {actual}
"""
ADDITIONAL_CALL_ENTRIES = '          {actual}\n'

NEVER = 0

_configurators = {}
_patch_entries = []
_call_entries = []


class UnitTests(TestCase):

    def setUp(self):
        self.set_up()

    def tearDown(self):
        self.tear_down()
        undo_patches()

    def set_up(self):
        """ Override this method to set up your unit test environment """
        pass

    def tear_down(self):
        """ Override this method to tear down your unit test environment """
        pass


class FluentAnyArguments(object):
    pass


ANY_ARGUMENTS = FluentAnyArguments()


class FluentTarget(object):

    def __init__(self, target):
        if isinstance(target, ModuleType):
            self._target_name = target.__name__
            self._target = import_module(self._target_name)
        else:
            target_type = type(target)
            self._target_name = target_type.__module__ + '.' + target_type.__name__
            self._target = target


class FluentAnswer(object):

    class ReturnAnswer(object):

        def __init__(self, value):
            self._value = value

        def __call__(self):
            return self._value

    class RaiseAnswer(object):

        def __init__(self, value):
            self._value = value

        def __call__(self):
            raise self._value

    def __init__(self, arguments, kwargs):
        self.arguments = arguments
        self.kwargs = kwargs
        self._answers = []

    def next(self):
        if len(self._answers) == 0:
            return None

        if len(self._answers) == 1:
            answer = self._answers[0]

        if len(self._answers) > 1:
            answer = self._answers.pop(0)

        return answer()

    def append_answer(self, answer_class, value):
        answer = answer_class(value)
        self._answers.append(answer)

    def then_return(self, value):
        self.append_answer(self.ReturnAnswer, value)
        return self

    def then_raise(self, value):
        self.append_answer(self.RaiseAnswer, value)
        return self


class FluentPatchEntry(FluentTarget):

    def __init__(self, target, attribute_name, original):
        FluentTarget.__init__(self, target)
        self._attribute_name = attribute_name
        self._original = original
        self._patch = None
        self._mock = None
        self._full_qualified_target_name = None

    def patch_away_with(self, fluent_mock):
        if isinstance(self._target, Mock):
            setattr(self._target, self._attribute_name, fluent_mock)
        else:
            self._full_qualified_target_name = self._target_name + '.' + self._attribute_name
            self._patch = patch(self._full_qualified_target_name)
            self._mock = self._patch.__enter__()
            self._mock.side_effect = fluent_mock

    def undo(self):
        if self._patch:
            self._patch.__exit__()


class FluentCallEntry(FluentTarget):

    def __init__(self, target, attribute, arguments, keyword_arguments):
        FluentTarget.__init__(self, target)
        self._attribute_name = attribute
        self._arguments = arguments
        self._keyword_arguments = keyword_arguments

    def verify(self, target, attribute_name, arguments, keyword_arguments):
        if self._target == target and self._attribute_name == attribute_name:
            if self._arguments == arguments and self._keyword_arguments == keyword_arguments:
                return True

        return False

    def __repr__(self):
        target_string = 'call {target_name}.{attribute_name}'.format(target_name=self._target_name,
                                                                     attribute_name=self._attribute_name)
        call_string = str(call(*self._arguments, **self._keyword_arguments))
        return call_string.replace('call', target_string)


class FluentMock(FluentTarget):

    def __init__(self, target, attribute_name):
        FluentTarget.__init__(self, target)
        self._attribute_name = attribute_name
        self._answers = []

    def __call__(self, *arguments, **keyword_arguments):
        call_entry = FluentCallEntry(self._target, self._attribute_name, arguments, keyword_arguments)
        _call_entries.append(call_entry)

        for answer in self._answers:
            if answer.arguments == arguments and answer.kwargs == keyword_arguments:
                return answer.next()
            if answer.arguments and answer.arguments[0] == ANY_ARGUMENTS:
                return answer.next()

        return None

    def append_new_answer(self, answer):
        self._answers.append(answer)


class FluentMockConfigurator(object):

    def __init__(self, mock):
        self._mock = mock
        self._arguments = None
        self._answer = None
        self._keyword_arguments = None

    def __call__(self, *arguments, **keyword_arguments):
        self._arguments = arguments
        self._keyword_arguments = keyword_arguments
        self._answer = FluentAnswer(self._arguments, self._keyword_arguments)
        self._mock.append_new_answer(self._answer)
        return self._answer


class FluentWhen(FluentTarget):

    def __init__(self, target):
        FluentTarget.__init__(self, target)

    def _get_original_attribute(self, name):

        if not hasattr(self._target, name):
            raise InvalidAttributeError(self._target_name, name)

        return getattr(self._target, name)

    def __getattr__(self, name):
        original = self._get_original_attribute(name)
        patch_entry = FluentPatchEntry(self._target, name, original)
        _patch_entries.append(patch_entry)

        key = (self._target, name)
        if not key in _configurators:
            fluent_mock = FluentMock(self._target, name)
            mock_configurator = FluentMockConfigurator(fluent_mock)
            patch_entry.patch_away_with(fluent_mock)
            _configurators[key] = mock_configurator

        return _configurators[key]


class InvalidAttributeError(Exception):

    def __init__(self, target_name, attribute_name):
        error_message = MESSAGE_INVALID_ATTRIBUTE.format(target_name=target_name, attribute_name=attribute_name)
        super(InvalidAttributeError, self).__init__(error_message)


class Verifier(FluentTarget):

    def __init__(self, target, times):
        FluentTarget.__init__(self, target)
        self._attribute_name = None
        self._times = times

        if times not in [0, 1]:
            raise NotImplementedError('Times can be 0 or 1.')

    def __getattr__(self, name):
        self._attribute_name = name

        if not hasattr(self._target, name):
            raise InvalidAttributeError(self._target_name, name)

        return self

    def _assert_called(self, *arguments, **keyword_arguments):
        expected_call_entry = FluentCallEntry(self._target, self._attribute_name, arguments, keyword_arguments)

        if not _call_entries:
            raise AssertionError(MESSAGE_NO_CALLS.format(expected=expected_call_entry))

        for call_entry in _call_entries:
            if call_entry.verify(self._target, self._attribute_name, arguments, keyword_arguments):
                return

        found_calls = []

        for call_entry in _call_entries:
            if call_entry._target == self._target and call_entry._attribute_name == self._attribute_name:
                found_calls.append(call_entry)

        number_of_found_calls = len(found_calls)
        if number_of_found_calls > 0:
            error_message = MESSAGE_EXPECTED_BUT_WAS.format(expected=expected_call_entry, actual=found_calls[0])
            if number_of_found_calls > 1:
                for call_entry in found_calls[1:]:
                    error_message += ADDITIONAL_CALL_ENTRIES.format(actual=call_entry)
            raise AssertionError(error_message)

        raise AssertionError(MESSAGE_COULD_NOT_VERIFY.format(expected=expected_call_entry))

    def _assert_never_called(self, *arguments, **keyword_arguments):
        for call_entry in _call_entries:
            if call_entry.verify(self._target, self._attribute_name, arguments, keyword_arguments):
                error_message = MESSAGE_HAS_BEEN_CALLED_AT_LEAST_ONCE.format(call_entry=call_entry)
                raise AssertionError(error_message)

    def __call__(self, *arguments, **keyword_arguments):
        if self._times == 0:
            self._assert_never_called(*arguments, **keyword_arguments)
        else:
            self._assert_called(*arguments, **keyword_arguments)


def when(target):
    return FluentWhen(target)


def undo_patches():
    global _call_entries, _patch_entries, _configurators

    for patch_entry in _patch_entries:
        patch_entry.undo()

    _call_entries = []
    _patch_entries = []
    _configurators = {}


def get_patches():
    return _patch_entries


def verify(target, times=1):
    return Verifier(target, times)
