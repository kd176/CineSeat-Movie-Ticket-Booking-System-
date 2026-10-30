"""
CineSeat - Movie Ticket Booking System (Python DSA Edition)
Main Runner Script
Student: Khushi (Registration No. 251302194)
Faculty Evaluator: Mr. Vivek
Course: Data Structures and Algorithms in Python
"""

import sys
import unittest


def run_tests():
    print("=" * 60)
    print("Running CineSeat Data Structures & Algorithms Unit Tests...")
    print("=" * 60)
    suite = unittest.defaultTestLoader.discover("tests", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["--cli", "-c", "cli"]:
            import cli
            cli.main()
            return
        elif arg in ["--test", "-t", "test"]:
            run_tests()
            return

    # Default: launch Web Application
    import app
    port = 5000
    print(f"================================================================")
    print(f" CineSeat Python DSA Movie Ticket Booking System")
    print(f" Student: Khushi (Reg No: 251302194) | Faculty: Mr. Vivek")
    print(f" Web Server running at: http://127.0.0.1:{port}")
    print(f" Tip: Run 'python main.py --cli' for Interactive Terminal mode")
    print(f"      Run 'python main.py --test' to run DSA Unit Tests")
    print(f"================================================================")
    app.app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
