import unittest
import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Import higher-order function decorators
from fp_decorators.higher_order import higher_order, memoize

# Import functions from FlaskBB for reference
from flaskbb.deprecation import deprecated, FlaskBBDeprecation


class TestHigherOrderIntegration(unittest.TestCase):

    def test_higher_order_decorator(self):
        """Test applying the higher_order decorator to a function."""

        # Apply the higher_order decorator to a function similar to format_date
        @higher_order(enhanced=True)
        def format_date(value, format=None):
            """Returns a formatted date string."""
            if format is None:
                format = "%Y-%m-%d"
            if isinstance(value, datetime):
                return value.strftime(format)
            return value

        # Test that the basic function works
        test_date = datetime(2023, 4, 20)
        result = format_date(test_date)
        self.assertEqual(result, "2023-04-20")

        # Test that the enhanced methods are available
        self.assertTrue(hasattr(format_date, 'compose'))
        self.assertTrue(hasattr(format_date, 'pipe'))
        self.assertTrue(hasattr(format_date, 'curry'))
        self.assertTrue(hasattr(format_date, 'partial'))

        # Test a simple use of the partial method to create a specialized formatter
        short_date = format_date.partial(format="%d/%m/%Y")
        self.assertEqual(short_date(test_date), "20/04/2023")

    def test_memoize_decorator(self):
        """Test applying the memoize decorator to a function."""

        # Track how many times the function is called
        call_count = 0

        # Apply the memoize decorator to a function similar to time_since
        @memoize
        def time_since(time):
            """Returns a string representing time since e.g. 3 days ago."""
            nonlocal call_count
            call_count += 1

            # Return a simple string for testing
            if isinstance(time, datetime):
                return f"Time since {time.strftime('%Y-%m-%d')}"
            return f"Time since {time}"

        # Call the function multiple times with the same input
        input_date = datetime(2023, 4, 20)

        # First call should execute the function
        result1 = time_since(input_date)
        self.assertEqual(call_count, 1)
        self.assertEqual(result1, "Time since 2023-04-20")

        # Second call with the same input should use the cache
        result2 = time_since(input_date)
        self.assertEqual(call_count, 1)  # Still 1, used cache
        self.assertEqual(result2, "Time since 2023-04-20")

        # Call with a different input should execute the function again
        result3 = time_since("another date")
        self.assertEqual(call_count, 2)  # Incremented, didn't use cache
        self.assertEqual(result3, "Time since another date")


if __name__ == '__main__':
    unittest.main()