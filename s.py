# Sudoku Solver - work of Justin Tan Vern Tze
# Design Doc - https://docs.google.com/document/d/1KCCfjfKg8iyMkaLdQSvfWO71qLnZUjACPIxyBmeREjo/edit?usp=sharing

# Imports
import csv

# Functions
def print_matrix(inputMatrix):
    for x in range(9):
        firstIndexInRow = 0 + (9 * x)
        rowOf9Numbers = inputMatrix[firstIndexInRow:firstIndexInRow+9]
        if isinstance(inputMatrix,list):
            centredNumbers = [f'{y["val"]:^3}' for y in rowOf9Numbers]
        elif isinstance(inputMatrix,str):
            centredNumbers = [f'{y:^3}' for y in rowOf9Numbers]
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
    for idx,masterCell in enumerate(master):
        
        # set individual cell value
        masterCell["val"] = quesString[idx]
        
        # row
        rowNo = str((idx // 9) + 1)
        masterCell["rowNo"] = rowNo
        
        # col    
        colNo = str((idx % 9) + 1)
        masterCell["colNo"] = colNo
        
        # mtx
        if masterCell["rowNo"] in ("1","2","3"):
            if masterCell["colNo"] in ("1","2","3"):
                mtxNo = "1"
            elif masterCell["colNo"] in ("4","5","6"):
                mtxNo = "2"
            elif masterCell["colNo"] in ("7","8","9"):
                mtxNo = "3"
        elif masterCell["rowNo"] in ("4","5","6"):
            if masterCell["colNo"] in ("1","2","3"):
                mtxNo = "4"
            elif masterCell["colNo"] in ("4","5","6"):
                mtxNo = "5"
            elif masterCell["colNo"] in ("7","8","9"):
                mtxNo = "6"
        elif masterCell["rowNo"] in ("7","8","9"):
            if masterCell["colNo"] in ("1","2","3"):
                mtxNo = "7"
            elif masterCell["colNo"] in ("4","5","6"):
                mtxNo = "8"
            elif masterCell["colNo"] in ("7","8","9"):
                mtxNo = "9"
        masterCell["mtxNo"] = mtxNo
        
        # add cell references to 9blocks
        master9block["rows"][rowNo]["cells"].append(masterCell)
        master9block["cols"][colNo]["cells"].append(masterCell)
        master9block["mtxs"][mtxNo]["cells"].append(masterCell)
    
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

    def solution_algorithm_1(cellSA1):
        # implement solution
        if len(cellSA1["sol"]) != 1:return
        currentSolution = cellSA1["sol"][0]
        cellSA1["val"] = currentSolution
        print(f"Solution found: (R,C={cellSA1['rowNo']},{cellSA1['colNo']}) "
            f"for value ({currentSolution})")
        print_matrix(master)
        # update solutions in 9block cells
        cellSA1["sol"] = []
        for rcmType,rcmNo in rcmTuple:
            for otherCell in master9block[rcmType][cellSA1[rcmNo]]["cells"]:
                try:otherCell["sol"].remove(currentSolution)
                except:pass
            master9block[rcmType][cellSA1[rcmNo]]["sols"][currentSolution] = []
            # print(f"emptied out {rcmType}{cellSA1[rcmNo]}'s ({currentSolution}) solution locations.")
        
    # def solution_algorithm_2(solSA2,solutionsSA2):
    #     if len(solutionsSA2[solSA2]) != 1:return
    #     cellSA2 = solutionsSA2[solSA2][0]
    #     cellSA2["val"] = solSA2
    #     print(f"Solution found: (R,C={cellSA2['rowNo']},{cellSA2['colNo']}) "
    #         f"for value ({solSA2})\n")
    #     print_matrix(master)
    #     solutionsSA2[solSA2] = []
    #     for rcmType,rcmNo in rcmTuple:
    #         for otherCell in master9block[rcmType][cellSA2[rcmNo]]["cells"]:
    #             try:otherCell["sol"].remove(solSA2)
    #             except:pass
    #         master9block[rcmType][cellSA2[rcmNo]]["sols"][solSA2] = []
        

    # Iteration Mechanism
    while True:
        for rcmType,rcmNo in rcmTuple:
            for currentRCM in master9block[rcmType]:
                cellsInCurrentRCM = master9block[rcmType][currentRCM]["cells"]
                for currentCell in cellsInCurrentRCM:
                    solution_algorithm_1(currentCell)
        # for rcmType,rcmNo in rcmTuple:
        #     for currentRCM in master9block[rcmType]:
        #         solsInCurrentRCM = master9block[rcmType][currentRCM]["sols"]
        #         for currentSol in solsInCurrentRCM:
        #             solution_algorithm_2(currentSol,solsInCurrentRCM)
        finalAnswer = ''.join([elem["val"] for elem in master])
        if finalAnswer == ansString:
            # currentSolveCount += 1
            # print(f"Sudoku #{currentSolveCount} of {totalSudokuCount} "\
            #     "has been solved.")
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

# Print Answer
# print_matrix(sample2[1])

# Proper - Run Program
""" totalSudokuCount = 0
currentSolveCount = 0
filename = "sudoku_small.csv"
file = open(filename)
csvreader = csv.reader(file)
for line in csvreader:
    totalSudokuCount += 1
file = open(filename)
csvreader = csv.reader(file)
for line in csvreader:
    question,answer = line
    overall_solve(question,answer) """