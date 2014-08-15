# fluentmock [![Build Status](https://travis-ci.org/aelgru/fluentmock.png?branch=master)](https://travis-ci.org/aelgru/fluentmock)

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

