# fluentmock [![Build Status](https://travis-ci.org/aelgru/fluentmock.png?branch=master)](https://travis-ci.org/aelgru/fluentmock) [![](https://pypip.in/v/fluentmock/badge.png)](http://pypi.python.org/pypi/fluentmock) [![](https://pypip.in/d/fluentmock/badge.png)](http://pypi.python.org/pypi/fluentmock) [![](https://pypip.in/license/fluentmock/badge.png)](http://pypi.python.org/pypi/fluentmock)

Fluent interface facade for Michael Foord's Mock.
- [X] Easy and readable configuration of mock side effects.
- [X] Configuration and verification using matchers.

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

## Matchers

_fluentmock_ offers a lot of matchers. You can use then in mock configuration or in verification.
```python
    def test_matching_any_integer_value(self):

        when(targetpackage).targetfunction(any_value_of_type(int)).then_return('argument was an integer')
        assert_that(targetpackage.targetfunction(13), equal_to('argument was an integer'))
        assert_that(targetpackage.targetfunction(42), equal_to('argument was an integer'))

    def test_matching_any_string_value(self):

        when(targetpackage).targetfunction(any_value_of_type(str)).then_return('argument was a string')
        assert_that(targetpackage.targetfunction('Hello'), equal_to('argument was a string'))
        assert_that(targetpackage.targetfunction('World'), equal_to('argument was a string'))
```

If you prefer to use constants instead of convenience functions _fluentmock_ comes with these constants for matching:
```python
ANY_BOOLEAN
ANY_DICTIONARY
ANY_FLOAT
ANY_INTEGER
ANY_LIST
ANY_SLICE
ANY_STRING
ANY_TUPLE
ANY_VALUE
ANY_VALUES
```

## Requirements

If you are working on Python 2.6 please install Brett Cannon's [importlib](http://pypi.python.org/pypi/importlib):

```bash
easy_install importlib
```

or

```bash
pip install importlib
```

## Documentation

* [Comparing Mock and Fluentmock](https://github.com/aelgru/fluentmock/blob/master/docs/COMPARISON.md)
* [Migrating from Mockito to Fluentmock](https://github.com/aelgru/fluentmock/blob/master/docs/MIGRATION.md)

