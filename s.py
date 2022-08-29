# Sudoku Solver - work of Justin Tan Vern Tze
# Design Doc - https://docs.google.com/document/d/1KCCfjfKg8iyMkaLdQSvfWO71qLnZUjACPIxyBmeREjo/edit?usp=sharing

# Imports
import csv

# Functions
def print_matrix(inputMatrix):
    for x in range(9):
        firstIndexInRow = 0 + (9 * x)
        rowOf9Numbers = inputMatrix[firstIndexInRow:firstIndexInRow+9]
        centredNumbers = [f'{y["val"]:^3}' for y in rowOf9Numbers]
        boxedCentredNumbers = "|".join(centredNumbers)
        print(boxedCentredNumbers)
        if x < 8:
            print("-" * len(boxedCentredNumbers))
    print()     

def overall_solve(quesString,ansString):

    global totalSudokuCount
    global currentSolveCount

    # 9block Mechanism
    rcmTuple = (("rows","rowNo"),(("cols","colNo")),(("mtxs","mtxNo")))
    master9block = {rcmType:{str(x):{"cells":[],
                                    "sols":{str(y):[] for y in range (1,10)},
                                    "spaces":0}
                            for x in range (1,10)}
                    for rcmType,rcmNo in rcmTuple}

    # Cell Mechanism
    master = [{"val":"", "sol":[], "rowNo":"", "colNo":"", "mtxNo":""}
            for x in range(81)]
    for idx,cell in enumerate(master):
        
        # set individual cell value
        cell["val"] = quesString[idx]
        
        # row
        rowNo = str((idx // 9) + 1)
        cell["rowNo"] = rowNo
        
        # col    
        colNo = str((idx % 9) + 1)
        cell["colNo"] = colNo
        
        # mtx
        if cell["rowNo"] in ("1","2","3"):
            if cell["colNo"] in ("1","2","3"):
                mtxNo = "1"
            elif cell["colNo"] in ("4","5","6"):
                mtxNo = "2"
            elif cell["colNo"] in ("7","8","9"):
                mtxNo = "3"
        elif cell["rowNo"] in ("4","5","6"):
            if cell["colNo"] in ("1","2","3"):
                mtxNo = "4"
            elif cell["colNo"] in ("4","5","6"):
                mtxNo = "5"
            elif cell["colNo"] in ("7","8","9"):
                mtxNo = "6"
        elif cell["rowNo"] in ("7","8","9"):
            if cell["colNo"] in ("1","2","3"):
                mtxNo = "7"
            elif cell["colNo"] in ("4","5","6"):
                mtxNo = "8"
            elif cell["colNo"] in ("7","8","9"):
                mtxNo = "9"
        cell["mtxNo"] = mtxNo
        
        # add cell references to 9blocks
        master9block["rows"][rowNo]["cells"].append(cell)
        master9block["cols"][colNo]["cells"].append(cell)
        master9block["mtxs"][mtxNo]["cells"].append(cell)

    print_matrix(master)
    
    # Solution-generator Mechanism
    numberList = [str(x) for x in range(1,10)]
    for currentCell in master:
        if currentCell["val"] != "0":continue
        possibleSolutions = numberList.copy()
        for rcmType,rcmNo in rcmTuple:
            for otherCell in master9block[rcmType][currentCell[rcmNo]]["cells"]:
                try:possibleSolutions.remove(otherCell["val"])
                except:pass
        """ print(f"Possible solutions for cell R,C:"
            f"{currentCell['rowNo']},{currentCell['colNo']} "
            f"of value {currentCell['val']} is {possibleSolutions}") """
        currentCell["sol"] = possibleSolutions
        
    # Populate 9block Solutions
    for rcmType,rcmNo in rcmTuple:
        for currentRCM in master9block[rcmType]:
            cellsInCurrentRCM = master9block[rcmType][currentRCM]["cells"]
            solsInCurrentRCM = master9block[rcmType][currentRCM]["sols"]
            for currentCell in cellsInCurrentRCM:
                for potentSol in currentCell["sol"]:
                    solsInCurrentRCM[potentSol].append(currentCell)
    # 9block Solutions Debugger
    """ for rcmType,rcmNo in rcmTuple:
        for currentRCM in master9block[rcmType]:
            solsInCurrentRCM = master9block[rcmType][currentRCM]["sols"]
            for a,b in solsInCurrentRCM.items():
                if len(b) < 1:continue
                print(rcmType,currentRCM,a,[(elem["rowNo"],elem["colNo"])
                                            for elem in b]) """

    def solution_algorithm_1(cell):
        # implement solution
        if len(cell["sol"]) != 1:return
        currentSolution = cell["sol"][0]
        cell["val"] = currentSolution
        """ print(f"Solution found: (R,C={cell['rowNo']},{cell['colNo']}) "
            f"for value ({currentSolution})\n")
        print_matrix() """
        # update solutions in 9block cells
        cell["sol"] = []
        for rcmType,rcmNo in rcmTuple:
            for otherCell in master9block[rcmType][cell[rcmNo]]["cells"]:
                try:otherCell["sol"].remove(currentSolution)
                except:pass
            master9block[rcmType][cell[rcmNo]]["sols"][currentSolution] = []
            print(f"emptied out {rcmType}{cell[rcmNo]}'s ({currentSolution}) solution locations.")
        
    # def solution_algorithm_2(solutions,sol):
    #     if len(solutions[sol]) != 1:return
    #     solutions[sol][0]["val"] = sol
    #     solutions[sol] = []
    #     # remove solution locations from similar solutions within RCM
    #     for rcmType,rcmNo in rcmTuple:
    #         for otherCell in master9block[rcmType][cell[rcmNo]]["cells"]:
    #             try:otherCell["sol"].remove(currentSolution)
    #             except:pass
        

    # Iteration Mechanism
    # while True:
    while True:
        for rcmType,rcmNo in rcmTuple:
            for currentRCM in master9block[rcmType]:
                cellsInCurrentRCM = master9block[rcmType][currentRCM]["cells"]
                solsInCurrentRCM = master9block[rcmType][currentRCM]["sols"]
                for currentCell in cellsInCurrentRCM:
                    solution_algorithm_1(currentCell)
                # for currentSol in solsInCurrentRCM:
                #     solution_algorithm_2(solsInCurrentRCM,currentSol)
        finalAnswer = ''.join([elem["val"] for elem in master])
        if finalAnswer == ansString:
            """ currentSolveCount += 1
            print(f"Sudoku #{currentSolveCount} of {totalSudokuCount} "\
                "has been solved.") """
            print("Sudoku solved...")
            break
        else:continue


# Playground - 9block printer
""" debug_matrix(False)
print()
while True:
    inp9b = input("What 9block do you want? >")
    if inp9b == "done":break
    while True:
        inpNo = input(f"Which {inp9b} do you want? >")
        if inpNo == "back":break
        if (int(inpNo)<1) or (int(inpNo)>9):continue
        for thing in master9block[inp9b][inpNo]["cells"]:print(thing)
        print()
        debug_matrix(False)
        print() """

# Development - Run Program
sample1 = "500104090006030002091070003070000060650001904930408500240605087800302005000040100","523184796786539412491276853174953268658721934932468571249615387817392645365847129"
sample2 = "068700900004000071030809050300080100040005007007304092602001005000020600059030028","568712943924653871731849256395287164246195387817364592682971435473528619159436728"
overall_solve(sample1[0],sample1[1])

# Proper - Run Program
""" totalSudokuCount = 0
currentSolveCount = 0
filename = "sudoku_small_3611.csv"
file = open(filename)
csvreader = csv.reader(file)
for line in csvreader:
    totalSudokuCount += 1
file = open(filename)
csvreader = csv.reader(file)
for line in csvreader:
    question,answer = line
    overall_solve(question,answer) """