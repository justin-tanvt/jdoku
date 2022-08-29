# Sudoku Solver - work of Justin Tan Vern Tze
# Design Doc - https://docs.google.com/document/d/1KCCfjfKg8iyMkaLdQSvfWO71qLnZUjACPIxyBmeREjo/edit?usp=sharing

# Functions
def print_matrix(input_matrix):
    for x in range(9):
        first_index_in_row = 0 + (9 * x)
        row_of_numbers = input_matrix[first_index_in_row:first_index_in_row+9]
        formatted_list = [f'{y["val"]:^3}' for y in row_of_numbers]
        spaced_string = "|".join(formatted_list)
        print(spaced_string)
        if x < 8:
            print("-" * len(spaced_string))
        
def mat(row,column):
    index_within_row = column - 1
    elem_from_rows_above = 9 * (row - 1)
    final_index = elem_from_rows_above + index_within_row
    return final_index

def debug_matrix(option):
    print_matrix(master)
    if option:
        for x in range(9):
            row = x * 9
            for y in master[row:row+9]:print(y)
            print()

# Example String
sample_string = "004300209005009001070060043006002087190007400"\
                "050083000600000105003508690042910300"

# 9block Mechanism
""" master_9block = {
                 "row":{
                        "cells" :{str(x):[] for x in range (1,10)},
                        "sols"  :{str(x):[] for x in range (1,10)},
                        "spaces":{str(x):0 for x in range (1,10)}
                        }, 
                 "col":{
                        "cells" :{str(x):[] for x in range (1,10)},
                        "sols"  :{str(x):[] for x in range (1,10)},
                        "spaces":{str(x):0 for x in range (1,10)}
                        },
                 "mtx":{
                        "cells" :{str(x):[] for x in range (1,10)},
                        "sols"  :{str(x):[] for x in range (1,10)},
                        "spaces":{str(x):0 for x in range (1,10)}
                        },
                 } """
master_9block = {
                 "row":{str(x):{"cells":[],"rows":[],"spaces":0} for x in \
                            range (1,10)
                        }, 
                 "col":{str(x):{"cells":[],"rows":[],"spaces":0} for x in \
                            range (1,10)
                        },
                 "mtx":{str(x):{"cells":[],"rows":[],"spaces":0} for x in \
                            range (1,10)
                        },
                 }

# Cell Mechanism
master = [{"val":"", "sol":[], "row_no":"", "col_no":"", "mtx_no":""} for x in 
          range(81)]
for idx,cell in enumerate(master):
    
    # set individual cell value
    cell["val"] = sample_string[idx]
    
    # row
    row_no = str((idx // 9) + 1)
    cell["row_no"] = row_no
    
    # col    
    col_no = str((idx % 9) + 1)
    cell["col_no"] = col_no
    
    # mtx
    if cell["row_no"] in ("1","2","3"):
        if cell["col_no"] in ("1","2","3"):
            mtx_no = "1"
        elif cell["col_no"] in ("4","5","6"):
            mtx_no = "2"
        elif cell["col_no"] in ("7","8","9"):
            mtx_no = "3"
    elif cell["row_no"] in ("4","5","6"):
        if cell["col_no"] in ("1","2","3"):
            mtx_no = "4"
        elif cell["col_no"] in ("4","5","6"):
            mtx_no = "5"
        elif cell["col_no"] in ("7","8","9"):
            mtx_no = "6"
    elif cell["row_no"] in ("7","8","9"):
        if cell["col_no"] in ("1","2","3"):
            mtx_no = "7"
        elif cell["col_no"] in ("4","5","6"):
            mtx_no = "8"
        elif cell["col_no"] in ("7","8","9"):
            mtx_no = "9"
    cell["mtx_no"] = mtx_no
    
    # 9block
    master_9block["row"][row_no]["cells"].append(cell)
    master_9block["col"][col_no]["cells"].append(cell)
    master_9block["mtx"][mtx_no]["cells"].append(cell)

# Playground
debug_matrix(False)
print()
while True:                                                     # 9block checker
    inp_9b = input("What 9block do you want? >")
    if inp_9b == "done":break
    while True:
        inp_no = input(f"Which {inp_9b} do you want? >")
        if inp_no == "back":break
        if (int(inp_no)<1) or (int(inp_no)>9):continue
        for thing in master_9block[inp_9b][inp_no]["cells"]:print(thing)
        print()
        debug_matrix(False)
        print()