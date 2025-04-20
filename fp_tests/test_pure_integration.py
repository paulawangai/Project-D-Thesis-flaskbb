import unittest
import sys
import os
import warnings

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Import the pure decorator
from fp_decorators.pure import pure

# Import the functions we're testing
from flaskbb.deprecation import deprecated, FlaskBBDeprecation, RemovedInFlaskBB3
from flaskbb.utils.helpers import crop_title

class TestPureIntegration(unittest.TestCase):

    def test_deprecated_decorator_purity(self):
        """Test that the deprecated decorator is pure."""

        # Create a test class for deprecation warnings
        class TestDeprecation(FlaskBBDeprecation):
            version = (4, 0, 0)

        # Create a message to use in the decorator
        test_message = "This is a test deprecation message"

        # Get the decorator with the test message and category
        decorator1 = deprecated(message=test_message, category=TestDeprecation)

        # Get another decorator with the same parameters - should behave identically
        decorator2 = deprecated(message=test_message, category=TestDeprecation)

        # Define a simple function to decorate
        def test_func():
            return "test"

        # Decorate the function with both decorators
        decorated1 = decorator1(test_func)
        decorated2 = decorator2(test_func)

        # Check that both decorated functions return the same result
        self.assertEqual(decorated1(), decorated2())

        # Check that the decorated function still works
        self.assertEqual(decorated1(), "test")

        # Check that the docstring is updated properly
        self.assertIn(test_message, decorated1.__doc__)

        # Verify decorator doesn't modify its input parameters
        test_message_copy = test_message
        decorator3 = deprecated(message=test_message, category=TestDeprecation)
        self.assertEqual(test_message, test_message_copy)

    def test_crop_title_purity(self):
        """Test that the crop_title function is pure."""

        # Test with various inputs
        test_cases = [
            # title, length, result
            ("This is a test title", 20, "This is a test title"),
            ("This is a longer test title that should be cropped", 20, "This is a longer..."),
            ("", 10, ""),
            ("Short", 10, "Short"),
        ]

        for title, length, expected in test_cases:
            # Make copies of inputs to verify they don't get modified
            title_copy = title
            length_copy = length

            # Call the function
            result = crop_title(title, length)

            # Verify inputs weren't modified
            self.assertEqual(title, title_copy)
            self.assertEqual(length, length_copy)

            # Verify result
            self.assertEqual(result, expected)

            # Call again to ensure consistent results
            result2 = crop_title(title, length)
            self.assertEqual(result, result2)


if __name__ == '__main__':
    unittest.main()