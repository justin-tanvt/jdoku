# Sudoku Solver - work of Justin Tan Vern Tze
# Design Doc - https://docs.google.com/document/d/1KCCfjfKg8iyMkaLdQSvfWO71qLnZUjACPIxyBmeREjo/edit?usp=sharing


# Imports
import csv
from time import perf_counter
import timeit


# Load CSV of sudokus [default = "sudoku_data.csv"]
filename = "sudoku_data.csv"


# Constants
NUMBER_LIST = [str(x) for x in range(1, 10)]
FAILURE_THRESHOLD_SECONDS = 0.5


# Functions
def print_matrix(inputMatrix):
    """ Prints formatted 9x9 matrix from given (list of dicts) or (string)."""
    for x in range(9):
        firstIndexInRow = 0 + (9 * x)
        rowOf9Numbers = inputMatrix[firstIndexInRow:(firstIndexInRow + 9)]
        if isinstance(inputMatrix, list):
            centredNumbers = [
                f'{y["val"]:^3}' 
                for y in rowOf9Numbers
            ]
        elif isinstance(inputMatrix, str):
            centredNumbers = [
                f'{y:^3}' 
                for y in rowOf9Numbers
            ]
        boxedCentredNumbers = "|".join(centredNumbers)
        print(boxedCentredNumbers)
        if x < 8:   # Don't print after row 9
            print("-" * len(boxedCentredNumbers))
    print()

def master_index(row, column):
    """Returns index between 0-81 from given (row,column) integer inputs."""
    indexWithinRow = column - 1
    elemCountFromPreviousRows = 9 * (row - 1)
    finalIndex = elemCountFromPreviousRows + indexWithinRow
    return finalIndex

def overall_solve(quesString, ansString):
    global solveCount
    global failCount
    global totalComputeTimeMseconds
    global failCases
    
    solveStartTime = perf_counter()
    
    # Used to iterate through rows/cols/mtxs in 9block master data structure
    rcmTuple = (
        ("rows", "rowNo"),
        ("cols", "colNo"),
        ("mtxs", "mtxNo")
    )
    
    # 9block Mechanism
    ## Represent each 9block as a dictionary in a master dictionary
    master9block = {
        # There are 3 types of 9blocks - rows/cols/mtxs(a.k.a. box)
        rcmType:{
            # Each type of 9block has 9 unique units - ie. 9 rows, 9 columns...
            str(x):{
                # Each 9block contains 9 cells to be contained in a list
                "cells":[],
                # Each 9block must contain the solutions 1-9
                "sols":{
                    # Potential solution locations to be contained in a list
                    str(y):[] 
                    for y in range (1,10)
                }
            }
            for x in range (1,10)
        }
        for rcmType, rcmNo in rcmTuple
    }

    # Cell Mechanism
    ## Represent each cell as a dictionary in a master list
    master = [
        {
            "val": "",
            "sol": [],
            "rowNo": "",
            "colNo": "",
            "mtxNo": ""
        }
        for x in range(81)
    ]
    for idxInMaster, cellInMaster in enumerate(master):
        # Fill in cell values from given question
        cellInMaster["val"] = quesString[idxInMaster]
        # Each cell belongs to a row, column & matrix 9block
        # Assign row, column and matrix numbers
        rowNo = str((idxInMaster // 9) + 1)
        cellInMaster["rowNo"] = rowNo
        colNo = str((idxInMaster % 9) + 1)
        cellInMaster["colNo"] = colNo
        if cellInMaster["rowNo"] in ("1", "2", "3"):
            if cellInMaster["colNo"] in ("1", "2", "3"):
                mtxNo = "1"
            elif cellInMaster["colNo"] in ("4", "5", "6"):
                mtxNo = "2"
            elif cellInMaster["colNo"] in ("7", "8", "9"):
                mtxNo = "3"
        elif cellInMaster["rowNo"] in ("4", "5", "6"):
            if cellInMaster["colNo"] in ("1", "2", "3"):
                mtxNo = "4"
            elif cellInMaster["colNo"] in ("4", "5", "6"):
                mtxNo = "5"
            elif cellInMaster["colNo"] in ("7", "8", "9"):
                mtxNo = "6"
        elif cellInMaster["rowNo"] in ("7", "8", "9"):
            if cellInMaster["colNo"] in ("1", "2", "3"):
                mtxNo = "7"
            elif cellInMaster["colNo"] in ("4", "5", "6"):
                mtxNo = "8"
            elif cellInMaster["colNo"] in ("7", "8", "9"):
                mtxNo = "9"
        cellInMaster["mtxNo"] = mtxNo
        # Append the cell into each of its 3 9blocks
        master9block["rows"][rowNo]["cells"].append(cellInMaster)
        master9block["cols"][colNo]["cells"].append(cellInMaster)
        master9block["mtxs"][mtxNo]["cells"].append(cellInMaster)

    # Solution-generator Mechanism
    for currentCell in master:
        if currentCell["val"] != "0": continue
        # Remove other numbers found in each of its 3 9blocks
        possibleSolutions = NUMBER_LIST.copy()
        for rcmType, rcmNo in rcmTuple:
            for otherCell in master9block[rcmType][currentCell[rcmNo]]["cells"]:
                try: possibleSolutions.remove(otherCell["val"])
                except: pass
        # Numbers remaining are the cell's possible solutions
        currentCell["sol"] = possibleSolutions
        
    # Populate 9block Possible-Solution-Locations
    for rcmType, rcmNo in rcmTuple:
        all9blocksOfSameType = master9block[rcmType]
        for current9block in all9blocksOfSameType:
            cellsIn9block = master9block[rcmType][current9block]["cells"]
            solsIn9block = master9block[rcmType][current9block]["sols"]
            for currentCell in cellsIn9block:
                # Iterate through each cell's potential solutions
                for potentSol in currentCell["sol"]:
                    # Append that cell in that 9block's solution's locations
                    solsIn9block[potentSol].append(currentCell)

    # Answer-checking Mechanism
    def check_answer(answerCell, solutionToCheckFor, printBool=False):
        correctAnswer = ansString[
            master_index(
                int(answerCell['rowNo']),
                int(answerCell['colNo'])
            )
        ]
        if solutionToCheckFor == correctAnswer:
            if printBool:print("This is indeed the correct solution")
        else:
            print("There has been an incorrect solution")
            print(f"{rcmType}{answerCell[rcmNo]}")
            print(
                f"correct answer:{correctAnswer} | "\
                f"computed answer:{solutionToCheckFor}"
            )
            print("Quitting program now...")
            quit()

    # Naked Single Algorithm
    ## Solve if that cell has only 1 potential solution
    def solution_algorithm_1(cellSA1):
        if len(cellSA1["sol"]) != 1: return
        currentSolution = cellSA1["sol"][0]
        cellSA1["val"] = currentSolution
        check_answer(cellSA1, currentSolution)
        cellSA1["sol"] = []
        for rcmType, rcmNo in rcmTuple:
            for otherCell in master9block[rcmType][cellSA1[rcmNo]]["cells"]:
                try: otherCell["sol"].remove(currentSolution)
                except: pass
            master9block[rcmType][cellSA1[rcmNo]]["sols"][currentSolution] = []
        
    # Hidden Single Algorithm
    ## Solve if that solution has only 1 potential location
    def solution_algorithm_2(solSA2, solutionsSA2):
        if len(solutionsSA2[solSA2]) != 1: return
        cellSA2 = solutionsSA2[solSA2][0]
        currentSolution = solSA2
        cellSA2["val"] = currentSolution
        cellSA2["sol"] = []
        check_answer(cellSA2, solSA2)
        solutionsSA2[solSA2] = []
        for rcmType, rcmNo in rcmTuple:
            for otherCell in master9block[rcmType][cellSA2[rcmNo]]["cells"]:
                try: otherCell["sol"].remove(solSA2)
                except: pass
            master9block[rcmType][cellSA2[rcmNo]]["sols"][solSA2] = []

    # Iteration Mechanism
    while True:
        for rcmType, rcmNo in rcmTuple:
            for current9block in master9block[rcmType]:
                cellsIn9block = master9block[rcmType][current9block]["cells"]
                for currentCell in cellsIn9block:
                    solution_algorithm_1(currentCell)
        for rcmType, rcmNo in rcmTuple:
            for current9block in master9block[rcmType]:
                solsIn9block = master9block[rcmType][current9block]["sols"]
                for currentSol in solsIn9block:
                    solution_algorithm_2(currentSol, solsIn9block)    
                    
        finalAnswer = ''.join([cell["val"] for cell in master])
        
        if finalAnswer == ansString:
            solveEndTime = perf_counter()
            elapsedTimeSeconds = solveEndTime - solveStartTime
            elapsedTimeMseconds = 1000 * elapsedTimeSeconds
            totalComputeTimeMseconds += elapsedTimeMseconds
            solveCount += 1
            averageComputeTimeMS = totalComputeTimeMseconds / solveCount  
            print(
                f"#{currentSudokuNo:>7n} | "\
                f"Solved:{solveCount:>7n} "\
                f"Failed:{failCount:>2n} | "\
                f"Current Time:{elapsedTimeMseconds:>6.3f}ms | "\
                f"Average Time:{averageComputeTimeMS:>6.3f}ms "
            )
            break
        # Timeout Mechanism
        elif (perf_counter() - solveStartTime) > FAILURE_THRESHOLD_SECONDS:
            failCount += 1
            print(
                f"#{currentSudokuNo:>7n} | "\
                f"Solved:{solveCount:>7n} "\
                f"Failed:{failCount:>2n} "
            )
            failCases.append(currentSudokuNo)
            break
        # Run through both algorithms again if still unsolved
        else:continue


# Run Program
programStartTime = timeit.default_timer()

solveCount = 0
failCount = 0
totalComputeTimeMseconds = 0
failCases = []

file = open(filename)
csvreader = csv.reader(file)
header = next(csvreader)      # Kaggle CSV has 'quizzes,solutions' on 1st line
for lineIndex,line in enumerate(csvreader):
    currentSudokuNo = lineIndex + 1
    (question, answer) = line
    overall_solve(question, answer)

programEndTime = timeit.default_timer()
totalTimeSeconds = programEndTime - programStartTime
totalTimeMins = totalTimeSeconds / 60
totalComputeTimeMinutes = totalComputeTimeMseconds / 1000 / 60

# Print Results
print()
print(f"| Summary |")
print(f"Solved:{solveCount:<7n}")
print(f"Failed:{failCount:<2n}")
print()
print(f"Average Compute Time: {totalComputeTimeMseconds / solveCount:<.3f}ms")
print(f"Total Compute Time: {totalComputeTimeMinutes:<.2f} minutes")
print(f"Total Time: {totalTimeMins:<.2f} minutes")
print()
print(f"Solve Rate: {100 * solveCount / (solveCount + failCount):<.4f}%")
print()
print(f"These are the following failed cases:\n{failCases}")
