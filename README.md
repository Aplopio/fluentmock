# *fluentmock*
[![Build Status](https://travis-ci.org/aelgru/fluentmock.png?branch=master)](https://travis-ci.org/aelgru/fluentmock)
[![PyPI version](https://badge.fury.io/py/fluentmock.png)](http://badge.fury.io/py/fluentmock)

Fluent interface for mock.

```python
from hamcrest import assert_that, equal_to
from fluentmock import UnitTests, when, verify

import targetpackage


class ExampleTests(UnitTests):

    def test_should_return_configured_value(self):

        when(targetpackage).targetfunction(2).then_return(3)
        assert_that(targetpackage.targetfunction(2), equal_to(3))
        verify(targetpackage).targetfunction(2)

    def test_should_return_configured_values_in_given_order(self):

        when(targetpackage).targetfunction(2).then_return(1).then_return(2).then_return(3)

        assert_that(targetpackage.targetfunction(2), equal_to(1))
        assert_that(targetpackage.targetfunction(2), equal_to(2))
        assert_that(targetpackage.targetfunction(2), equal_to(3))

        verify(targetpackage).targetfunction(2)

    def test_should_repeatedly_return_last_configured_value(self):

        when(targetpackage).targetfunction(2).then_return(1).then_return(5)

        targetpackage.targetfunction(2)

        assert_that(targetpackage.targetfunction(2), equal_to(5))
        assert_that(targetpackage.targetfunction(2), equal_to(5))
        assert_that(targetpackage.targetfunction(2), equal_to(5))

        verify(targetpackage).targetfunction(2)
```
## License

fluentmock is licensed under the
[Apache License, Version 2.0](https://raw.github.com/aelgru/fluentmock/master/src/main/python/fluentmock/LICENSE.txt)
