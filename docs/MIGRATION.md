# Migrating from Mockito to Fluentmock

## mockito.mock → mock.Mock

Since _fluentmock_ is a facade for _mock_ you can replace the import of `mock` from mockito with `Mock` from mock.

mockito:
```python
from mockito import mock
```

Fluentmock:
```python
from mock import Mock
```

## unittest.TestCase + mockito.unstub → fluentmock.UnitTests

Replace the usage of class `TestCase` from unittest with fluentmock's class `UnitTests`.
UnitTests will undo the patches after execution and offers you a nice way to stick with the underscore convention for
method names.

mockito:
```python
import unittest

class Tests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        pass
```

Fluentmock:
```python
from fluentmock import UnitTests

class Tests(UnitTests):

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def test(self):
        pass
```

## mockito.any → fluentmock.ANY_VALUE or fluentmock.ANY_VALUES

Replace the call to `any()` with the Matcher `ANY_VALUES`
when you want to make sure the target has been called with any argument(s).
But use the matcher `ANY_VALUE` if you want to match the
`ANY_VALUE` works here like a wildcard (think *) for a argument.

## thenReturn → then_return

Fluentmock uses the underscore convention for method names.

## thenRaise → then_raise

Fluentmock uses the underscore convention for method names.
