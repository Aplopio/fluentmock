# *fluentmock*
[![Build Status](https://travis-ci.org/aelgru/fluentmock.png?branch=master)](https://travis-ci.org/aelgru/fluentmock)
[![PyPI version](https://badge.fury.io/py/fluentmock.png)](http://badge.fury.io/py/fluentmock)

Fluent interface for mock.

```python
from hamcrest import assert_that, equal_to
from fluentmock import UnitTests, when, verify

import targetpackage


class ExampleTest(UnitTests):

    def should_return_configured_value_three_when_called(self):

        when(targetpackage).targetfunction().then_return(3)

        assert_that(targetpackage.targetfunction(), equal_to(3))

        verify(targetpackage).targetfunction()
```
## License

fluentmock is licensed under the
[Apache License, Version 2.0](https://raw.github.com/aelgru/fluentmock/master/src/main/python/fluentmock/LICENSE.txt)

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/aelgru/fluentmock/trend.png)](https://bitdeli.com/free "Bitdeli Badge")
