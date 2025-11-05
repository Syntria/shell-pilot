# Assuming your function is in 'functions/run_python_file.py'
from functions.run_python_file import run_python_file

def run_all_tests():
    """Runs all test cases for the run_python_file function."""
    
    print("--- Test Case 1: Run main.py with no arguments ---")
    result1 = run_python_file("calculator", "main.py")
    print(result1)
    print("-" * 20)

    print("--- Test Case 2: Run main.py with arguments ---")
    result2 = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result2)
    print("-" * 20)

    print("--- Test Case 3: Run the tests.py file ---")
    result3 = run_python_file("calculator", "tests.py")
    print(result3)
    print("-" * 20)

    print("--- Test Case 4: Attempt directory traversal attack ---")
    result4 = run_python_file("calculator", "../main.py")
    print(result4)
    print("-" * 20)

    print("--- Test Case 5: Attempt to run a non-existent file ---")
    result5 = run_python_file("calculator", "nonexistent.py")
    print(result5)
    print("-" * 20)

if __name__ == "__main__":
    run_all_tests()
