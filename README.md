# *fluentmock*
[![Build Status](https://travis-ci.org/aelgru/fluentmock.png?branch=master)](https://travis-ci.org/aelgru/fluentmock)
[![PyPi version](https://pypip.in/v/fluentmock/badge.png)](https://crate.io/packages/fluentmock/)
[![PyPi downloads](https://pypip.in/d/fluentmock/badge.png)](https://crate.io/packages/fluentmock/)

A mocking framework with a fluent interface.

```python
from hamcrest import assert_that, equal_to
from fluentmock import UnitTests, when, verify

import targetpackage


class Example(UnitTests):

    def should_return_configured_value_three_when_called(self):

        when(targetpackage).targetfunction().then_return(3)

        assert_that(targetpackage.targetfunction(), equal_to(3))

        verify(targetpackage).targetfunction()
```
## License

fluentmock is licensed under the
[Apache License, Version 2.0](https://raw.github.com/aelgru/fluentmock/master/src/main/python/fluentmock/LICENSE.txt)
