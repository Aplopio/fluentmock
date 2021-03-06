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

from unittest import TestCase

from hamcrest import assert_that, equal_to
from fluentmock import when, undo_patches, get_patches

import targetpackage


class UndoPatchesTests(TestCase):

    def test_should_undo_patching_of_function(self):

        when(targetpackage).patch_test_1().then_return('patched!')

        undo_patches()

        assert_that(targetpackage.patch_test_1(), equal_to('not patched 1'))

    def test_should_undo_patching_of__multiple_functions(self):

        when(targetpackage).patch_test_1().then_return('patched call! 1')
        when(targetpackage).patch_test_2().then_return('patched call! 2')

        undo_patches()

        assert_that(targetpackage.patch_test_1(), equal_to('not patched 1'))
        assert_that(targetpackage.patch_test_2(), equal_to('not patched 2'))

    def test_should_reset_list_of_patches(self):

        when(targetpackage).patch_test_1().then_return('patched call! 1')
        when(targetpackage).patch_test_2().then_return('patched call! 2')

        undo_patches()

        assert_that(get_patches(), equal_to([]))
