# Migrating from Mockito to Fluentmock

## mockito.mock -> mock.Mock

Since _fluentmock_ is a facade for _mock_ you can replace the import of `mock` from mockito with `Mock` from mock.

Legacy:
```python
from mockito import mock
```

Fluentmock:
```python
from mock import Mock
```

## unittest.TestCase -> fluentmock.UnitTests

Replace the usage of class `TestCase` from unittest with fluentmock's class `UnitTests`.
UnitTests will undo the patches after execution and offers you a nice way to stick with the underscore convention for
method names.

Legacy:
```python
import unittest

class Tests(unittest.TestCase):

    def setUp(self):
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

    def test(self):
        pass
```

## mockito.any -> fluentmock.ANY_ARGUMENTS

Replace the call to `any()` with a `ANY_ARGUMENTS`.

## thenReturn -> then_return

Fluentmock uses the underscore convention for method names.

## thenRaise -> then_raise

Fluentmock uses the underscore convention for method names.
