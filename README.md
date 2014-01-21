# *fluentmock*
[![Build Status](https://travis-ci.org/aelgru/fluentmock.png?branch=master)](https://travis-ci.org/aelgru/fluentmock)
[![PyPI version](https://badge.fury.io/py/fluentmock.png)](http://badge.fury.io/py/fluentmock)

Fluent interface for Michael Foord's mock.

A example test using _fluentmock_ and hamcrest:
```python
from fluentmock import UnitTests, when, verify
from hamcrest import assert_that, equal_to


class SeveralAnswersTests(UnitTests):
  def test_should_return_configured_values_in_given_order(self):

    when(targetpackage).targetfunction(2).then_return(1).then_return(2).then_return(3)

    assert_that(targetpackage.targetfunction(2), equal_to(1))
    assert_that(targetpackage.targetfunction(2), equal_to(2))
    assert_that(targetpackage.targetfunction(2), equal_to(3))

    verify(targetpackage).targetfunction(2)
```

## Comparing Mock with Fluentmock

Here is a simple test example which configures a mock with a "side effect" in such a way it returns 3 when 2 is given
as a argument.
```python
from unittest import TestCase
from mock import patch


class MockStyleTest(TestCase):

    @patch('targetpackage.targetfunction')
    def test_should_return_configured_value(self, mock_targetfunction):

        def side_effect(argument):
            if argument == 2:
                return 3
            return None

        mock_targetfunction.side_effect = side_effect

        self.assertEqual(targetpackage.targetfunction(2), 3)

        mock_targetfunction.assert_called_with(2)
```

Here is a equivalent written using _fluentmock_:
```python
from fluentmock import UnitTests, when, verify


class FluentmockStyleTest(UnitTests):

    def test_should_return_configured_value(self):

        when(targetpackage).targetfunction(2).then_return(3)

        self.assertEqual(targetpackage.targetfunction(2), 3)

        verify(targetpackage).targetfunction(2)
```

## Motivation

... was to replace mockito with something that is as powerful as Mock.

## License

fluentmock is licensed under the
[Apache License, Version 2.0](https://raw.github.com/aelgru/fluentmock/master/src/main/python/fluentmock/LICENSE.txt)
