#!/usr/bin/env python3
import os
import subprocess
import time
from pathlib import Path

def run_all_solutions():
    """Run all Advent of Code 2015 solutions and display results."""
    
    # Get the directory where this script is located
    base_dir = Path(__file__).parent
    
    # Colors for terminal output
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}  Advent of Code 2015 - Running All Solutions{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")
    
    total_time = 0
    results = []
    
    # Run solutions for days 1-25
    for day in range(1, 26):
        day_dir = base_dir / f"day{day}"
        solve_file = day_dir / "solve.py"
        
        if not solve_file.exists():
            results.append({
                'day': day,
                'status': 'missing',
                'output': 'solve.py not found',
                'time': 0
            })
            continue
        
        print(f"{BOLD}Day {day:2d}:{RESET} ", end='', flush=True)
        
        start_time = time.time()
        try:
            # Run the solution
            result = subprocess.run(
                ['python3', 'solve.py'],
                cwd=day_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            elapsed = time.time() - start_time
            total_time += elapsed
            
            if result.returncode == 0:
                output = result.stdout.strip()
                if output and "Not yet implemented" not in output:
                    status = 'success'
                    print(f"{GREEN}✓{RESET} ({elapsed:.3f}s)")
                else:
                    status = 'not_implemented'
                    output = "Not yet implemented"
                    print(f"{YELLOW}○{RESET} Not implemented")
            else:
                status = 'error'
                output = result.stderr.strip() if result.stderr else result.stdout.strip()
                print(f"{RED}✗{RESET} Error")
            
            results.append({
                'day': day,
                'status': status,
                'output': output,
                'time': elapsed
            })
            
        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            total_time += elapsed
            results.append({
                'day': day,
                'status': 'timeout',
                'output': 'Execution timed out (>30s)',
                'time': elapsed
            })
            print(f"{RED}✗{RESET} Timeout")
        except Exception as e:
            elapsed = time.time() - start_time
            total_time += elapsed
            results.append({
                'day': day,
                'status': 'error',
                'output': str(e),
                'time': elapsed
            })
            print(f"{RED}✗{RESET} Exception: {e}")
    
    # Print detailed results
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}  Detailed Results{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")
    
    for result in results:
        day = result['day']
        status = result['status']
        output = result['output']
        elapsed = result['time']
        
        if status == 'success':
            print(f"{BOLD}Day {day:2d}:{RESET} {GREEN}✓ Success{RESET} ({elapsed:.3f}s)")
            # Print output with indentation
            for line in output.split('\n'):
                if line.strip():
                    print(f"  {line}")
        elif status == 'not_implemented':
            print(f"{BOLD}Day {day:2d}:{RESET} {YELLOW}○ Not yet implemented{RESET}")
        elif status == 'missing':
            print(f"{BOLD}Day {day:2d}:{RESET} {RED}✗ Missing{RESET}")
            print(f"  {output}")
        else:
            print(f"{BOLD}Day {day:2d}:{RESET} {RED}✗ {status.title()}{RESET}")
            # Print first few lines of error
            error_lines = output.split('\n')[:3]
            for line in error_lines:
                if line.strip():
                    print(f"  {line}")
        print()
    
    # Print summary
    print(f"{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}  Summary{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    not_impl_count = sum(1 for r in results if r['status'] == 'not_implemented')
    error_count = sum(1 for r in results if r['status'] in ['error', 'timeout', 'missing'])
    
    print(f"  {GREEN}✓ Completed:{RESET}        {success_count}/25")
    print(f"  {YELLOW}○ Not Implemented:{RESET}  {not_impl_count}/25")
    print(f"  {RED}✗ Errors/Missing:{RESET}   {error_count}/25")
    print(f"  {BOLD}Total Time:{RESET}         {total_time:.3f}s")
    print()

if __name__ == '__main__':
    run_all_solutions()
