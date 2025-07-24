import os
import random
import subprocess
from datetime import datetime
from sudoku import Sudoku

os.environ['PATH'] = '/usr/local/bin:/usr/bin:/bin'
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

save_folder = "sudoku_files"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

def solve_sudoku():
    puzzle = Sudoku(3).difficulty(0.6)
    solution = puzzle.solve()
    return puzzle.board, solution.board

def save_to_file(puzzle, solution, filename):
    filepath = os.path.join(save_folder, filename)
    with open(filepath, "w") as file:
        file.write("Puzzle:\n")
        for i in range(9):
            file.write(" ".join(map(str, puzzle[i*9:(i+1)*9])) + "\n")
        file.write("\nSolution:\n")
        for row in solution:
            file.write(" ".join(map(str, row)) + "\n")
    return filepath

def git_operations(filepath):
    try:
        result = subprocess.run(['git', 'add', filepath], 
                              capture_output=True, text=True, cwd=script_dir)
        if result.returncode != 0:
            print(f"Git add failed: {result.stderr}")
            return False
        
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd=script_dir)
        if not result.stdout.strip():
            print("No changes to commit")
            return True
        
        commit_message = f"NYT daily Sudoku: {datetime.today().date()}"
        result = subprocess.run(['git', 'commit', '-m', commit_message], 
                              capture_output=True, text=True, cwd=script_dir)
        if result.returncode != 0:
            print(f"Git commit failed: {result.stderr}")
            return False
        
        print("Changes committed successfully")
        
        result = subprocess.run(['git', 'push'], 
                              capture_output=True, text=True, cwd=script_dir)
        if result.returncode == 0:
            print("Changes pushed to GitHub successfully")
            return True
        else:
            print(f"Git push failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Git operations error: {str(e)}")
        return False

def update_cron_with_random_time():
    try:
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        
        python_path = subprocess.run(['which', 'python3'], capture_output=True, text=True).stdout.strip()
        if not python_path:
            python_path = '/usr/bin/python3'
        
        new_cron_command = f"{random_minute} {random_hour} * * * cd {script_dir} && {python_path} {os.path.join(script_dir, 'sudoku_solver.py')} >> {os.path.join(script_dir, 'cron.log')} 2>&1\n"
        
        cron_file = "/tmp/current_cron"
        
        subprocess.run(['crontab', '-l'], stdout=open(cron_file, 'w'), stderr=subprocess.DEVNULL)
        
        try:
            with open(cron_file, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            lines = []
        
        with open(cron_file, "w") as file:
            for line in lines:
                if 'sudoku_solver.py' not in line:
                    file.write(line)
            file.write(new_cron_command)
        
        subprocess.run(['crontab', cron_file])
        os.remove(cron_file)
        
        print(f"Cron job updated to run at {random_hour:02d}:{random_minute:02d} daily")
        return True
        
    except Exception as e:
        print(f"Cron update error: {str(e)}")
        return False

def setup_git_for_cron():
    try:
        result = subprocess.run(['git', 'config', 'user.email'], 
                              capture_output=True, text=True, cwd=script_dir)
        if result.returncode != 0 or not result.stdout.strip():
            print("Git user.email not set. Please run:")
            print("git config --global user.email 'your-email@example.com'")
            print("git config --global user.name 'Your Name'")
            return False
        
        return True
    except Exception as e:
        print(f"Git setup error: {str(e)}")
        return False

def main():
    date = datetime.today().date()
    textfile = f"nyt_daily_sudoku_{date}.txt"
    
    print(f"Starting sudoku generation for {date}")
    
    try:
        if not setup_git_for_cron():
            exit(1)
        
        puzzle, solution = solve_sudoku()
        filepath = save_to_file(puzzle, solution, textfile)
        print(f"Sudoku saved to {filepath}")
        
        if git_operations(filepath):
            print("Git operations completed successfully")
        else:
            print("Git operations failed")
            exit(1)
        
        if update_cron_with_random_time():
            print("Cron job updated successfully")
        else:
            print("Cron job update failed")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()