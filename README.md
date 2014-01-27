[![PyPI version](https://badge.fury.io/py/fluentmock.png)](http://badge.fury.io/py/fluentmock)
[![Downloads](https://pypip.in/d/fluentmock/badge.png)](https://pypi.python.org/pypi/fluentmock)
[![Coverage Status](https://coveralls.io/repos/aelgru/fluentmock/badge.png)](https://coveralls.io/r/aelgru/fluentmock)
[![Build Status](https://travis-ci.org/aelgru/fluentmock.png?branch=master)](https://travis-ci.org/aelgru/fluentmock)
[![License](https://pypip.in/license/fluentmock/badge.png)](https://raw.github.com/aelgru/fluentmock/master/src/main/python/fluentmock/LICENSE.txt)

[![Logo](https://raw.github.com/aelgru/fluentmock/master/docs/fluentmock-logo.png)](https://pypi.python.org/pypi/fluentmock)

Fluent interface facade for Michael Foord's mock.

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

## Documentation

* [Comparing Mock and Fluentmock](https://github.com/aelgru/fluentmock/blob/master/docs/COMPARISON.md)

## Motivation

... was to replace mockito with something that is as powerful as Mock.
