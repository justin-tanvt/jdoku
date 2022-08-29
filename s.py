# Sudoku Solver - work of Justin Tan Vern Tze
# Design Doc - https://docs.google.com/document/d/1KCCfjfKg8iyMkaLdQSvfWO71qLnZUjACPIxyBmeREjo/edit?usp=sharing

# Functions
def print_matrix(inputMatrix):
    for x in range(9):
        firstIndexInRow = 0 + (9 * x)
        rowOfNumbers = inputMatrix[firstIndexInRow:firstIndexInRow+9]
        formattedList = [f'{y["val"]:^3}' for y in rowOfNumbers]
        spacedString = "|".join(formattedList)
        print(spacedString)
        if x < 8:
            print("-" * len(spacedString))
        
def master_index(row,column):
    indexWithinRow = column - 1
    elemFromRowsAbove = 9 * (row - 1)
    finalIndex = elemFromRowsAbove + indexWithinRow
    return finalIndex

def debug_matrix(option):
    print_matrix(master)
    if option:
        for x in range(9):
            row = x * 9
            for y in master[row:row+9]:print(y)
            print()

# Example String
sampleString = "004300209005009001070060043006002087190007400"\
                "050083000600000105003508690042910300"

# 9block Mechanism
master9block = {
                 "row":{str(x):{"cells":[],"sols":[],"spaces":0} for x in \
                            range (1,10)}, 
                 "col":{str(x):{"cells":[],"sols":[],"spaces":0} for x in \
                            range (1,10)},
                 "mtx":{str(x):{"cells":[],"sols":[],"spaces":0} for x in \
                            range (1,10)},
                 }

# Cell Mechanism
master = [{"val":"", "sol":[], "rowNo":"", "colNo":"", "mtxNo":""} for x in 
          range(81)]
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
    master9block["row"][rowNo]["cells"].append(cell)
    master9block["col"][colNo]["cells"].append(cell)
    master9block["mtx"][mtxNo]["cells"].append(cell)

# Solution-generator Mechanism
debug_matrix(False)
numberList = [str(x) for x in range(1,10)]
for currentCell in master:
    if currentCell["val"] != "0":continue
    possibleSolutions = numberList.copy()
    for otherCell in master9block["row"][currentCell["rowNo"]]["cells"]:
        try:possibleSolutions.remove(otherCell["val"])
        except:pass
    for otherCell in master9block["col"][currentCell["colNo"]]["cells"]:
        try:possibleSolutions.remove(otherCell["val"])
        except:pass
    for otherCell in master9block["mtx"][currentCell["mtxNo"]]["cells"]:
        try:possibleSolutions.remove(otherCell["val"])
        except:pass
    """ print(f"Possible solutions for cell R,C:"
          f"{currentCell['rowNo']},{currentCell['colNo']} "
          f"of value {currentCell['val']} is {possibleSolutions}") """
    currentCell["sol"] = possibleSolutions

# Playground
# debug_matrix(False)
# print()
# while True:                                                     # 9block checker
#     inp9b = input("What 9block do you want? >")
#     if inp9b == "done":break
#     while True:
#         inpNo = input(f"Which {inp9b} do you want? >")
#         if inpNo == "back":break
#         if (int(inpNo)<1) or (int(inpNo)>9):continue
#         for thing in master9block[inp9b][inpNo]["cells"]:print(thing)
#         print()
#         debug_matrix(False)
#         print()