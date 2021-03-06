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

import sys
from subprocess import STDOUT, call


def targetfunction():
    sys.stdout.write("WARNING! Actual function has been called.\n")


def patch_test_1():
    return 'not patched 1'


def patch_test_2():
    return 'not patched 2'


class TheClass(object):

    def some_method(self):
        sys.stdout.write("WARNING! Actual method has been called.\n")

    @classmethod
    def some_class_method(self):
        sys.stdout.write("WARNING! Actual method has been called.\n")


class TheOldStyleClass:

    def some_method(self):
        sys.stdout.write("WARNING! Actual method has been called.\n")

    @classmethod
    def some_class_method(self):
        sys.stdout.write("WARNING! Actual method has been called.\n")


def call_a_subprocess():
    call(['pip'], stderr=STDOUT)
