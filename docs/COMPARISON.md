# Comparing Mock with Fluentmock

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

