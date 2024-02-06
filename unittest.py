import subprocess
import unittest

class TestLinting(unittest.TestCase):
    def test_pylint(self):
        # Run Pylint as a subprocess
        pylint_output = subprocess.run(
            ['pylint', 'your_module.py', '--output-format=text'],
            capture_output=True,
            text=True
        ).stdout
        
        # Check if Pylint output contains specific messages
        self.assertNotIn('C0103', pylint_output, "Variable names should follow snake_case naming convention")
        self.assertNotIn('C0301', pylint_output, "Line too long")

if __name__ == '__main__':
    unittest.main()
