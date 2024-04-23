import tkinter as tk
import numpy as np
import sys

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku Solver")

        # Setup frames for the input and solution grids
        frame_input = tk.Frame(master)
        frame_input.grid(row=0, column=0, padx=(20, 10), pady=20)
        frame_solution = tk.Frame(master)
        frame_solution.grid(row=0, column=1, padx=(10, 20), pady=20)

        # Initialize grids and GUI components
        self.grid = np.zeros((9, 9), dtype=int)
        self.entries = [[tk.Entry(frame_input, width=3, font=('Arial', 18), justify='center') for _ in range(9)] for _ in range(9)]
        self.solution_entries = [[tk.Entry(frame_solution, width=3, font=('Arial', 18), justify='center', fg='blue') for _ in range(9)] for _ in range(9)]

        # Place entry widgets in the grid
        for i in range(9):
            for j in range(9):
                self.entries[i][j].grid(row=i, column=j, stick="nsew", padx=1, pady=1)
                self.solution_entries[i][j].grid(row=i, column=j, stick="nsew", padx=1, pady=1)

        # Add solve and clear buttons
        solve_button = tk.Button(master, text='Solve', command=self.solve)
        solve_button.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        clear_button = tk.Button(master, text='Clear', command=self.clear)
        clear_button.grid(row=1, column=1, sticky="ew", padx=20, pady=10)

    def solve(self):
        for i in range(9):
            for j in range(9):
                try:
                    self.grid[i][j] = int(self.entries[i][j].get())
                except ValueError:
                    self.grid[i][j] = 0

        if self.backtrack_solve(np.copy(self.grid), count_solutions=True):
            self.display_solution(self.grid)
        else:
            print("No solution exists", file=sys.stderr)

    def backtrack_solve(self, grid, count_solutions=False):
        if count_solutions:
            return self.count_solutions(grid) == 1

        find = self.find_empty_location(grid)
        if not find:
            return True
        row, col = find

        for num in range(1, 10):
            if self.is_safe(grid, row, col, num):
                grid[row][col] = num
                if self.backtrack_solve(grid):
                    return True
                grid[row][col] = 0
        return False

    def count_solutions(self, grid, limit=2):
        """Count solutions up to a specified limit."""
        find = self.find_empty_location(grid)
        if not find:
            return 1
        row, col = find
        solution_count = 0

        for num in range(1, 10):
            if self.is_safe(grid, row, col, num):
                grid[row][col] = num
                solution_count += self.count_solutions(grid, limit)
                grid[row][col] = 0
                if solution_count >= limit:
                    break  # Early exit if we reach the limit

        return solution_count

    def find_empty_location(self, grid):
        return next(((i, j) for i in range(9) for j in range(9) if grid[i][j] == 0), None)

    def is_safe(self, grid, row, col, num):
        box_x, box_y = (row // 3) * 3, (col // 3) * 3
        return all([
            num not in grid[row],  # Check row
            num not in grid[:, col],  # Check column
            num not in grid[box_x:box_x + 3, box_y:box_y + 3]  # Check box
        ])

    def display_solution(self, solved_grid):
        for i in range(9):
            for j in range(9):
                self.solution_entries[i][j].delete(0, tk.END)
                self.solution_entries[i][j].insert(0, str(solved_grid[i][j]))

    def clear(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.solution_entries[i][j].delete(0, tk.END)

def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
