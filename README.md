# SudoCommit
This Python script automatically fetches, solves, and saves daily Sudoku puzzles, then commits and pushes the solution to a Git repository. It also updates the system's cron job to run the script at a random time each day.

## Features

- **Fetch Sudoku Puzzle**: The script fetches a daily Sudoku puzzle from a specified URL (New York Times or similar sources).
- **Solve Puzzle**: The script solves the puzzle using a backtracking algorithm.
- **Save Puzzle and Solution**: It saves the original puzzle and its solution to a text file, formatted for readability.
- **Git Integration**: The solution is automatically committed to a Git repository with a message that includes today's date and then pushed to GitHub (or any other remote repository).
- **Cron Job**: The script updates the system's cron job to run at a random time each day to automate the puzzle-solving process.

## Prerequisites

Ensure that you have the following installed on your machine:

- **Python 3.6+**
- **Git** (for version control)

## Setup
1. Clone the repository
``` bash
git clone https://github.com/yourusername/sudoku-solver.git
cd sudoku-solver
```
2. Install dependencies
Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use .venv\\Scripts\\activate
```
Then install the dependencies:
```bash
pip install -r requirements.txt
```
3. Run Script
```bash
python sudoku_solver.py
```
