# *fluentmock* [![Build Status](https://travis-ci.org/aelgru/fluentmock.png?branch=master)](https://travis-ci.org/aelgru/fluentmock)

A mocking framework with a fluent interface.

```python
from unittest import TestCase
from fluentmock import when, unstub

import targetpackage


class ExampleTest(TestCase):

    def test_should_return_configured_value_three_when_called(self):
        when(targetpackage).targetfunction().then_return(3)

        actual = targetpackage.targetfunction()

        self.assertEqual(3, actual)

        unstub()
```
## License

fluentmock is licensed under the
[Apache License, Version 2.0](https://raw.github.com/aelgru/committer/master/src/main/python/committer/LICENSE.txt)
