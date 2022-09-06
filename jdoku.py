# Sudoku Solver - work of Justin Tan Vern Tze
# Design Doc - https://docs.google.com/document/d/1KCCfjfKg8iyMkaLdQSvfWO71qLnZUjACPIxyBmeREjo/edit?usp=sharing


# Imports
import csv
from time import perf_counter
import timeit


# Load CSV of sudokus [default = "sudoku_data.csv"]
filename = "sudoku_full.csv"


# Constants
numberList = [str(x) for x in range(1, 10)]
failureThresholdSeconds = 0.5


# Functions
def print_matrix(inputMatrix):
    """ Prints formatted 9x9 matrix of given (list of dicts) or (string)."""
    for x in range(9):
        firstIndexInRow = 0 + (9 * x)
        rowOf9Numbers = inputMatrix[firstIndexInRow:(firstIndexInRow + 9)]
        if isinstance(inputMatrix, list):
            centredNumbers = [f'{y["val"]:^3}' for y in rowOf9Numbers]
        elif isinstance(inputMatrix, str):
            centredNumbers = [f'{y:^3}' for y in rowOf9Numbers]
        boxedCentredNumbers = "|".join(centredNumbers)
        print(boxedCentredNumbers)
        if x < 8:   # Don't print after row 9
            print("-" * len(boxedCentredNumbers))
    print()

def master_index(row, column):
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
    
    # 9block Mechanism
    rcmTuple = (("rows", "rowNo"),(("cols", "colNo")),(("mtxs", "mtxNo")))
    master9block = {
        rcmType:{
            str(x):{"cells":[],
                    "sols":{str(y):[] for y in range (1,10)}}
            for x in range (1,10)}
        for rcmType,rcmNo in rcmTuple}

    # Cell Mechanism
    master = [
        {"val": "", "sol": [], "rowNo": "", "colNo": "", "mtxNo": ""}
        for x in range(81)
        ]
    for idx, masterCell in enumerate(master):
        masterCell["val"] = quesString[idx]
        rowNo = str((idx // 9) + 1)
        masterCell["rowNo"] = rowNo
        colNo = str((idx % 9) + 1)
        masterCell["colNo"] = colNo
        if masterCell["rowNo"] in ("1", "2", "3"):
            if masterCell["colNo"] in ("1", "2", "3"):
                mtxNo = "1"
            elif masterCell["colNo"] in ("4", "5", "6"):
                mtxNo = "2"
            elif masterCell["colNo"] in ("7", "8", "9"):
                mtxNo = "3"
        elif masterCell["rowNo"] in ("4", "5", "6"):
            if masterCell["colNo"] in ("1", "2", "3"):
                mtxNo = "4"
            elif masterCell["colNo"] in ("4", "5", "6"):
                mtxNo = "5"
            elif masterCell["colNo"] in ("7", "8", "9"):
                mtxNo = "6"
        elif masterCell["rowNo"] in ("7", "8", "9"):
            if masterCell["colNo"] in ("1", "2", "3"):
                mtxNo = "7"
            elif masterCell["colNo"] in ("4", "5", "6"):
                mtxNo = "8"
            elif masterCell["colNo"] in ("7", "8", "9"):
                mtxNo = "9"
        masterCell["mtxNo"] = mtxNo

        master9block["rows"][rowNo]["cells"].append(masterCell)
        master9block["cols"][colNo]["cells"].append(masterCell)
        master9block["mtxs"][mtxNo]["cells"].append(masterCell)

    # Solution-generator Mechanism
    for currentCell in master:
        if currentCell["val"] != "0":continue
        possibleSolutions = numberList.copy()
        for rcmType,rcmNo in rcmTuple:
            for otherCell in master9block[rcmType][currentCell[rcmNo]]["cells"]:
                try:possibleSolutions.remove(otherCell["val"])
                except:pass
        currentCell["sol"] = possibleSolutions
        
    # Populate 9block Possible-Solution-Locations
    for rcmType,rcmNo in rcmTuple:
        for currentRCM in master9block[rcmType]:
            cellsInCurrentRCM = master9block[rcmType][currentRCM]["cells"]
            solsInCurrentRCM = master9block[rcmType][currentRCM]["sols"]
            for currentCell in cellsInCurrentRCM:
                for potentSol in currentCell["sol"]:
                    solsInCurrentRCM[potentSol].append(currentCell)

    def check_answer(answerCell, solutionToCheckFor, printBool=False):
        correctAnswerToCheckAgainst = ansString[master_index(int(answerCell['rowNo']), int(answerCell['colNo']))]
        if solutionToCheckFor == correctAnswerToCheckAgainst:
            if printBool:print("This is indeed the correct solution")
        else:
            print("There has been an incorrect solution")
            print(f"{rcmType}{answerCell[rcmNo]}")
            print(f"correct answer:{correctAnswerToCheckAgainst} | computed answer:{solutionToCheckFor}")
            print("Quitting program now...")
            quit()

    def solution_algorithm_1(cellSA1):
        if len(cellSA1["sol"]) != 1:return
        currentSolution = cellSA1["sol"][0]
        cellSA1["val"] = currentSolution
        check_answer(cellSA1, currentSolution)
        cellSA1["sol"] = []
        for rcmType,rcmNo in rcmTuple:
            for otherCell in master9block[rcmType][cellSA1[rcmNo]]["cells"]:
                try:otherCell["sol"].remove(currentSolution)
                except:pass
            master9block[rcmType][cellSA1[rcmNo]]["sols"][currentSolution] = []
        
    def solution_algorithm_2(solSA2, solutionsSA2):
        if len(solutionsSA2[solSA2]) != 1:return
        cellSA2 = solutionsSA2[solSA2][0]
        cellSA2["val"] = solSA2
        cellSA2["sol"] = []
        check_answer(cellSA2, solSA2)
        solutionsSA2[solSA2] = []
        for rcmType,rcmNo in rcmTuple:
            for otherCell in master9block[rcmType][cellSA2[rcmNo]]["cells"]:
                try:otherCell["sol"].remove(solSA2)
                except:pass
            master9block[rcmType][cellSA2[rcmNo]]["sols"][solSA2] = []

    # Iteration Mechanism
    while True:
        for rcmType,rcmNo in rcmTuple:
            for currentRCM in master9block[rcmType]:
                cellsInCurrentRCM = master9block[rcmType][currentRCM]["cells"]
                for currentCell in cellsInCurrentRCM:
                    solution_algorithm_1(currentCell)
        for rcmType,rcmNo in rcmTuple:
            for currentRCM in master9block[rcmType]:
                solsInCurrentRCM = master9block[rcmType][currentRCM]["sols"]
                for currentSol in solsInCurrentRCM:
                    solution_algorithm_2(currentSol,solsInCurrentRCM)    
                    
        finalAnswer = ''.join([elem["val"] for elem in master])
        
        if finalAnswer == ansString:
            solveEndTime = perf_counter()
            elapsedTimeSeconds = solveEndTime - solveStartTime
            elapsedTimeMseconds = 1000 * elapsedTimeSeconds
            totalComputeTimeMseconds += elapsedTimeMseconds
            solveCount += 1
            averageComputeTimeMS = totalComputeTimeMseconds / solveCount  
            print(f"#{currentSudokuNo:>7n} | "\
                  f"Solved:{solveCount:>7n} "\
                  f"Failed:{failCount:>2n} | "\
                  f"Current Time:{elapsedTimeMseconds:>6.3f}ms | "\
                  f"Average Time:{averageComputeTimeMS:>6.3f}ms ")
            break
        elif (perf_counter() - solveStartTime) > failureThresholdSeconds:
            failCount += 1
            print(f"#{currentSudokuNo:>7n} | "\
                  f"Solved:{solveCount:>7n} "\
                  f"Failed:{failCount:>2n} ")
            failCases.append(currentSudokuNo)
            break
        else:continue


# Run Program
programStartTime = timeit.default_timer()

solveCount = 0
failCount = 0
totalComputeTimeMseconds = 0
failCases = []

file = open(filename)
csvreader = csv.reader(file)
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
print(f"Average Compute Time: {totalComputeTimeMseconds/solveCount:<.3f}ms")
print(f"Total Compute Time: {totalComputeTimeMinutes:<.2f} minutes")
print(f"Total Time: {totalTimeMins:<.2f} minutes")
print()
print(f"Solve Rate: {100*solveCount/1000000:<.4f}%")
print()
print(f"These are the following failed cases:\n{failCases}")