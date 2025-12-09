#!/usr/bin/env python3
"""
Advent of Code 2015 - Submission Helper
Opens browser tabs for each day and copies answers to clipboard for easy submission.
"""

import subprocess
import webbrowser
import time
import sys
from pathlib import Path

# Answers for all days (Part 1 and Part 2)
ANSWERS = {
    1: {"part1": "232", "part2": "1783"},
    2: {"part1": "1586300", "part2": "3737498"},
    3: {"part1": "2572", "part2": "2631"},
    4: {"part1": "254575", "part2": "1038736"},
    5: {"part1": "238", "part2": "69"},
    6: {"part1": "543903", "part2": "14687245"},
    7: {"part1": "3176", "part2": "14710"},
    8: {"part1": "1371", "part2": "2117"},
    9: {"part1": "141", "part2": "736"},
    10: {"part1": "329356", "part2": "4666278"},
    11: {"part1": "cqjxxyzz", "part2": "cqkaabcc"},
    12: {"part1": "111754", "part2": "65402"},
    13: {"part1": "709", "part2": "668"},
    14: {"part1": "2640", "part2": "1102"},
    15: {"part1": "21367368", "part2": "1766400"},
    16: {"part1": "40", "part2": "241"},
    17: {"part1": "1304", "part2": "18"},
    18: {"part1": "814", "part2": "924"},
    19: {"part1": "576", "part2": "207"},
    20: {"part1": "776160", "part2": "786240"},
    21: {"part1": "121", "part2": "201"},
    22: {"part1": "1824", "part2": "1937"},
    23: {"part1": "184", "part2": "231"},
    24: {"part1": "11266889531", "part2": "77387711"},
    25: {"part1": "9132360", "part2": "Merry Christmas!"},
}


def copy_to_clipboard(text):
    """Copy text to clipboard using pbcopy (macOS)."""
    try:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
        return True
    except Exception as e:
        print(f"  Warning: Could not copy to clipboard: {e}")
        return False


def submit_day(day, part=1):
    """Open browser for a specific day and copy answer to clipboard."""
    if day not in ANSWERS:
        print(f"Day {day} not found in answers.")
        return False

    part_key = f"part{part}"
    if part_key not in ANSWERS[day]:
        print(f"Day {day} Part {part} not found in answers.")
        return False

    answer = ANSWERS[day][part_key]
    url = f"https://adventofcode.com/2015/day/{day}"

    print(f"\n{'='*70}")
    print(f"Day {day} - Part {part}")
    print(f"{'='*70}")
    print(f"Answer: {answer}")
    print(f"URL: {url}")

    # Copy answer to clipboard
    if copy_to_clipboard(answer):
        print(f"✓ Answer copied to clipboard!")
    else:
        print(f"  (You can manually copy: {answer})")

    # Open browser
    print(f"Opening browser...")
    webbrowser.open(url)

    return True


def interactive_mode():
    """Interactive mode - submit one day at a time."""
    print("\n" + "="*70)
    print("  Advent of Code 2015 - Interactive Submission Helper")
    print("="*70)
    print("\nThis tool will:")
    print("  1. Open the Advent of Code page for each day")
    print("  2. Copy the answer to your clipboard")
    print("  3. You paste and click submit in the browser")
    print("\n" + "="*70 + "\n")

    while True:
        try:
            day_input = input("Enter day number (1-25) or 'q' to quit: ").strip().lower()

            if day_input == 'q' or day_input == 'quit':
                print("Goodbye!")
                break

            if not day_input.isdigit():
                print("Please enter a number between 1 and 25, or 'q' to quit.")
                continue

            day = int(day_input)
            if day < 1 or day > 25:
                print("Please enter a number between 1 and 25.")
                continue

            # Ask which part
            part_input = input(f"Which part for Day {day}? (1/2 or 'both'): ").strip().lower()

            if part_input == 'both':
                submit_day(day, 1)
                time.sleep(2)
                submit_day(day, 2)
            elif part_input in ['1', '2']:
                submit_day(day, int(part_input))
            else:
                print("Please enter '1', '2', or 'both'.")
                continue

            print("\nPress Enter when ready to continue...")
            input()

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def bulk_mode(start_day=1, end_day=25, delay=3):
    """Bulk mode - open all days in sequence with a delay."""
    print("\n" + "="*70)
    print("  Advent of Code 2015 - Bulk Submission Helper")
    print("="*70)
    print(f"\nOpening days {start_day} to {end_day}")
    print(f"Delay between submissions: {delay} seconds")
    print("\n" + "="*70 + "\n")

    for day in range(start_day, end_day + 1):
        # Part 1
        submit_day(day, 1)

        if day != end_day or True:  # Always show pause for part 2
            print(f"\nWaiting {delay} seconds before Part 2...")
            time.sleep(delay)

        # Part 2 (skip for day 25 if it's just "Merry Christmas!")
        if day != 25:
            submit_day(day, 2)

            if day != end_day:
                print(f"\nWaiting {delay} seconds before next day...")
                time.sleep(delay)

    print("\n" + "="*70)
    print("  All submissions ready!")
    print("="*70)


def main():
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == 'bulk':
            start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            end = int(sys.argv[3]) if len(sys.argv) > 3 else 25
            delay = int(sys.argv[4]) if len(sys.argv) > 4 else 3
            bulk_mode(start, end, delay)
        elif command == 'day':
            if len(sys.argv) < 3:
                print("Usage: python submit_helper.py day <day_number> [part]")
                return
            day = int(sys.argv[2])
            part = int(sys.argv[3]) if len(sys.argv) > 3 else 1
            submit_day(day, part)
        elif command == 'help':
            print_help()
        else:
            print(f"Unknown command: {command}")
            print_help()
    else:
        # Default to interactive mode
        interactive_mode()


def print_help():
    print("""
Advent of Code 2015 - Submission Helper

Usage:
  python submit_helper.py                    # Interactive mode
  python submit_helper.py bulk [start] [end] [delay]  # Bulk mode
  python submit_helper.py day <day> [part]   # Single day/part
  python submit_helper.py help               # Show this help

Examples:
  python submit_helper.py                    # Interactive mode
  python submit_helper.py bulk               # Submit all days (1-25)
  python submit_helper.py bulk 10 15 5       # Days 10-15, 5 sec delay
  python submit_helper.py day 5              # Day 5, Part 1
  python submit_helper.py day 5 2            # Day 5, Part 2

In all modes:
  - The browser opens to the day's page
  - The answer is copied to your clipboard
  - You paste and click submit manually
""")


if __name__ == '__main__':
    main()
