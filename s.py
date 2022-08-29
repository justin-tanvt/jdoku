# Sudoku Solver - work of Justin Tan Vern Tze
# Design Doc - https://docs.google.com/document/d/1KCCfjfKg8iyMkaLdQSvfWO71qLnZUjACPIxyBmeREjo/edit?usp=sharing

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
        
def master_index(row,column):
    indexWithinRow = column - 1
    elemCountFromPreviousRows = 9 * (row - 1)
    finalIndex = elemCountFromPreviousRows + indexWithinRow
    return finalIndex

def debug_matrix(option):
    print_matrix(master)
    if option:
        for x in range(9):
            firstIndexInRow = x * 9
            for y in master[firstIndexInRow:firstIndexInRow+9]:print(y)
            print()

# Example String
sampleString = "004300209005009001070060043006002087190007400"\
                "050083000600000105003508690042910300"

# 9block Mechanism
rcmTuple = (("rows","rowNo"),(("cols","colNo")),(("mtxs","mtxNo")))
master9block = {
                 "rows":{str(x):{"cells":[],
                                 "sols":{str(y):[] for y in range (1,10)},
                                 "spaces":0}
                         for x in range (1,10)}, 
                 "cols":{str(x):{"cells":[],
                                 "sols":{str(y):[] for y in range (1,10)},
                                 "spaces":0}
                         for x in range (1,10)},
                 "mtxs":{str(x):{"cells":[],
                                 "sols":{str(y):[] for y in range (1,10)},
                                 "spaces":0}
                         for x in range (1,10)},
                 }

# Cell Mechanism
master = [{"val":"", "sol":[], "rowNo":"", "colNo":"", "mtxNo":""}
          for x in range(81)]
for idx,cell in enumerate(master):
    
    # set individual cell value
    cell["val"] = sampleString[idx]
    
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

# Solution-generator Mechanism
numberList = [str(x) for x in range(1,10)]
for currentCell in master:
    if currentCell["val"] != "0":continue
    possibleSolutions = numberList.copy()
    for otherCell in master9block["rows"][currentCell["rowNo"]]["cells"]:
        try:possibleSolutions.remove(otherCell["val"])
        except:pass
    for otherCell in master9block["cols"][currentCell["colNo"]]["cells"]:
        try:possibleSolutions.remove(otherCell["val"])
        except:pass
    for otherCell in master9block["mtxs"][currentCell["mtxNo"]]["cells"]:
        try:possibleSolutions.remove(otherCell["val"])
        except:pass
    """ print(f"Possible solutions for cell R,C:"
          f"{currentCell['rowNo']},{currentCell['colNo']} "
          f"of value {currentCell['val']} is {possibleSolutions}") """
    currentCell["sol"] = possibleSolutions
    
# Populate 9block Solutions
# for currentRow in master9block["rows"]:
#     cellsInCurrentRow = master9block["rows"][currentRow]["cells"]
#     solsInCurrentRow = master9block["rows"][currentRow]["sols"]
#     for currentCell in cellsInCurrentRow:
#         for potentSol in currentCell["sol"]:
#             if cell in solsInCurrentRow[potentSol]:continue
#             solsInCurrentRow[potentSol].append(cell)
    
# Solution Algorithms
def solution_algorithm_1(cell):
    # implement solution
    if len(cell["sol"]) != 1:return
    currentSolution = cell["sol"][0]
    cell["val"] = currentSolution
    print(f"\nSolved cell R,C:{cell['rowNo']},{cell['colNo']} "
          f"for value {currentSolution}\n")
    # update solutions in 9block cells
    cell["sol"] = []
    for otherCell in master9block["rows"][cell["rowNo"]]["cells"]:
        try:otherCell["sol"].remove(currentSolution)
        except:pass
    for otherCell in master9block["cols"][cell["colNo"]]["cells"]:
        try:otherCell["sol"].remove(currentSolution)
        except:pass
    for otherCell in master9block["mtxs"][cell["mtxNo"]]["cells"]:
        try:otherCell["sol"].remove(currentSolution)
        except:pass
def solution_algorithm_2():
    pass

# Iteration Mechanism
# while True:
# for currentRow in master9block["rows"]:
#     cellsInCurrentRow = master9block["rows"][currentRow]["cells"]
#     solsInCurrentRow = master9block["rows"][currentRow]["sols"]
#     for currentCell in cellsInCurrentRow:
#         for potentSol in currentCell["sol"]:
#             if cell in solsInCurrentRow[potentSol]:continue
#             solsInCurrentRow[potentSol].append(cell)
#         solution_algorithm_1(currentCell)
#     iterate through sols
#         solution algo 2
#     pass
# for eachCol in master9block["cols"]:
#     pass
# for eachMtx in master9block["mtxs"]:
#     pass

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

# Playground - 3x3 mtx 1 onestep solver        
""" print_matrix(master)
def debug_mtx1():
    for cell in master9block["mtxs"]["1"]["cells"]:
        if cell["val"] != "0":continue
        print(f"Possible solutions for cell R,C:"
            f"{cell['rowNo']},{cell['colNo']} "
            f"of value {cell['val']} are {cell['sol']}")
debug_mtx1()
for cell in master9block["mtxs"]["1"]["cells"]:
    solution_algorithm_1(cell)
print_matrix(master)
debug_mtx1() """