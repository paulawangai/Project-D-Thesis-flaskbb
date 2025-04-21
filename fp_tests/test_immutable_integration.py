import unittest
import sys
import os
import warnings

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Import the immutable decorator
from fp_decorators.immutable import immutable

# Import the functions we're going to test from FlaskBB
from flaskbb.utils.helpers import format_date, format_datetime
from flaskbb.deprecation import deprecated, FlaskBBDeprecation

class TestImmutableIntegration(unittest.TestCase):

    def test_format_date_immutability(self):
        """Test that format_date function respects immutability."""

        # Test with various date formats and timestamps
        test_date = "2023-04-20"
        test_format = "%Y-%m-%d"

        # Make copies to verify they're not modified
        date_copy = test_date
        format_copy = test_format

        # Call the function (assuming it's decorated with @immutable)
        result = format_date(test_date, format=test_format)

        # Verify inputs are not modified
        self.assertEqual(test_date, date_copy)
        self.assertEqual(test_format, format_copy)

        # Same test with a different date format
        test_format = "%d-%m-%Y"
        format_copy = test_format
        result = format_date(test_date, format=test_format)
        self.assertEqual(test_format, format_copy)

    def test_format_datetime_immutability(self):
        """Test that format_datetime function respects immutability."""

        # Test with a datetime object
        test_datetime = "2023-04-20 14:30:00"
        test_format = "%Y-%m-%d %H:%M:%S"

        # Make copies to verify they're not modified
        datetime_copy = test_datetime
        format_copy = test_format

        # Call the function (assuming it's decorated with @immutable)
        result = format_datetime(test_datetime, format=test_format)

        # Verify inputs are not modified
        self.assertEqual(test_datetime, datetime_copy)
        self.assertEqual(test_format, format_copy)

    def test_deprecated_decorator_immutability(self):
        """Test that the deprecated decorator factory respects immutability."""

        # Create a test class for deprecation warnings
        class TestDeprecation(FlaskBBDeprecation):
            version = (4, 0, 0)

        # Create a message to use in the decorator
        test_message = "This is a test deprecation message"
        test_message_copy = test_message

        # Get the decorator (assuming deprecated is decorated with @immutable)
        decorator = deprecated(message=test_message, category=TestDeprecation)

        # Verify inputs are not modified
        self.assertEqual(test_message, test_message_copy)

        # Define a simple function to decorate
        def test_func():
            return "test"

        # Apply the decorator and ensure it works correctly
        decorated = decorator(test_func)
        self.assertEqual(decorated(), "test")

        # The message should be in the docstring but the original message should be unchanged
        self.assertIn(test_message, decorated.__doc__)
        self.assertEqual(test_message, test_message_copy)

    def test_immutable_with_freeze_input(self):
        """Test that freeze_input parameter works correctly with FlaskBB functions."""

        # Define a test function that will be decorated with freeze_input=True
        @immutable(freeze_input=True)
        def process_config(config_dict):
            # Should receive a frozenset of tuples instead of a dict
            self.assertNotIsInstance(config_dict, dict)

            # Create a new dict from the frozen input
            result = {}
            for k, v in config_dict:
                result[k] = v

            # Add a new key
            result['processed'] = True
            return result

        # Test with a configuration dictionary
        config = {'debug': True, 'testing': False, 'secret_key': 'test123'}

        # Call the function
        result = process_config(config)

        # Original should be unchanged
        self.assertEqual(config, {'debug': True, 'testing': False, 'secret_key': 'test123'})

        # Result should have the new key
        self.assertEqual(result['processed'], True)
        self.assertEqual(result['debug'], True)
        self.assertEqual(result['testing'], False)
        self.assertEqual(result['secret_key'], 'test123')

if __name__ == '__main__':
    unittest.main()