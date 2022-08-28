import csv
import numpy as np

file = open('sudoku_small.csv')
csvreader = csv.reader(file)
header = next(csvreader)
sample_set = next(csvreader)
num_dict = {str(i):None for i in range(1,10)}

def string_to_9x9(input_string):
    output_matrix = []
    for x in range(0,73,9):
        row_list = list(input_string[x:x+9])
        output_matrix.append(row_list)
    return np.array(output_matrix,dtype=np.dtype('U100'))
    
def potential_solutions(input_matrix,row,column):
    remaining_nums = num_dict.copy()
    current_row,current_column = input_matrix[row,:],input_matrix[:,column]
    for char in current_row:
        if char in remaining_nums: del remaining_nums[char]
    for char in current_column:
        if char in remaining_nums: del remaining_nums[char]
    return ''.join([num for num in remaining_nums])

def generate_solutions():
    seen_0 = False
    for row in range(9):
        for column in range(9):
            if m_ques[row,column] != "0": continue
            seen_0 = True
            d_sol[row,column] = potential_solutions(m_ques,row,column)
    if not seen_0: 
        solved = True
    print(d_sol)

def implement_solutions():
    no_available_solution = True
    for key,value in d_sol.items():
        if len(value) > 1: continue
        no_available_solution = False
        row,column = key
        m_ques[row,column] = value
        print(f"Solving R,C = {row+1},{column+1}")
        d_sol[key] = ""
    if no_available_solution:
        print('We have run out of potential solutions :(')
        print('Quitting Program...')
        quit()
    print(m_ques,"\n\n")
    
m_ques = string_to_9x9(sample_set[0])
m_ans = string_to_9x9(sample_set[1])
d_sol = dict()

print("SUDOKU BEFORE SOLVING:")
print(m_ques,"\n\n")

solved = False
while not solved:
    generate_solutions()
    implement_solutions()