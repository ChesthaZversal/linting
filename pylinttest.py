import subprocess
import unittest

class TestLinting(unittest.TestCase):
    def test_pylint(self):
        # Run Pylint as a subprocess
        pylint_output = subprocess.run(
            ['pylint', 'eliza.py', '--output-format=text'],
            capture_output=True,
            text=True
        ).stdout
        
        # Check if Pylint output contains specific messages
        self.assertNotIn('C0103', pylint_output, "Variable names should follow snake_case naming convention")
        self.assertNotIn('C0301', pylint_output, "Line too long")
        pylint_score = float(pylint_output.split('Your code has been rated at ')[1].split('/')[0].strip())
        
        # Check if Pylint score is more than 75
        self.assertGreaterEqual(pylint_score, 7.5, "Pylint score is less than 7.5")

if __name__ == '__main__':
    unittest.main()
