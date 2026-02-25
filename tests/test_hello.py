import io
import sys
import unittest
from hello import main

class TestHello(unittest.TestCase):
    def test_output(self):
        captured = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = captured
        try:
            main()
        finally:
            sys.stdout = sys_stdout
        self.assertEqual(captured.getvalue().strip(), "Hello, world!")

if __name__ == "__main__":
    unittest.main()
