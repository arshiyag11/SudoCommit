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

def git_commit(filename):
    subprocess.run(['git', 'add', filename])
    commit_message = f"NYT daily Sudoku: {datetime.today().date()}"
    subprocess.run(['git', 'commit', '-m', commit_message])

def git_push():
    result = subprocess.run(['git', 'push'], capture_output=True, text=True)
    if result.returncode == 0:
        print("Changes pushed to GitHub successfully.")
    else:
        print("Error pushing to GitHub:")
        print(result.stderr)

# Function to update the cron job with a random time
def update_cron_with_random_time():
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    new_cron_command = f"{random_minute} {random_hour} * * * cd {script_dir} && python3 {os.path.join(script_dir, 'sudoku_solver.py')}\n"
    
    cron_file = "/tmp/current_cron"
    os.system(f"crontab -l > {cron_file} 2>/dev/null || true") 
    
    with open(cron_file, "r") as file:
        lines = file.readlines()

    with open(cron_file, "w") as file:
        for line in lines:
            if 'sudoku_solver.py' not in line:
                file.write(line)
        file.write(new_cron_command)

    os.system(f"crontab {cron_file}")
    os.remove(cron_file)
    print(f"Cron job updated to run at {random_hour}:{random_minute} tomorrow.")

def main():
    date = datetime.today().date()
    textfile = f"nyt_daily_sudoku_{date}.txt" 
    
    try:
        puzzle, solution = solve_sudoku()
        save_to_file(puzzle, solution, textfile)
        git_commit(textfile)
        git_push()
        update_cron_with_random_time()

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
