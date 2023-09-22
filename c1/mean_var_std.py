import numpy as np

testarr = np.arange(0,9)
ex1 = [2,6,2,8,4,0,1,5,7]

def calculate(list):

    # They specifically said fewer than 9, not equal to 9. 
    # I just want to follow instructions on the exercises because I've found that when I do my own way 
    # it tends to get marked as wrong (not just for this set of challenges, I mean in general)
    if len(list) < 9:
        raise ValueError("List must contain nine numbers.")
    
    # I initially wanted to use a nons=[None,None,None] but this created a huge by-reference assignment headache
    # Since only 1 challenge and I'm not writing code for an actual project, I decided to just copy-paste 
    solutions_dict = {"mean" : [[None,None,None],[None,None,None],None],
                    "variance" : [[None,None,None],[None,None,None],None],
                    "standard deviation" : [[None,None,None],[None,None,None],None],
                    "max" : [[None,None,None],[None,None,None],None],
                    "min" : [[None,None,None],[None,None,None],None],
                    "sum" : [[None,None,None],[None,None,None],None]}

    # Reshape into the 3x3 as asked
    matrix = np.asarray(list).reshape(3,3)
    
    # This is the fastest way I could quickly think of to get this all done in good time
    for i in range(3):
        # Using : first gives you the ith entry of every row = ith column
        the_column = matrix[:, i]

        # Much faster to just use numpy's builtins than use the formulae
        solutions_dict["mean"][0][i] = the_column.mean()
        solutions_dict["variance"][0][i] = the_column.var()
        solutions_dict["standard deviation"][0][i] = the_column.std()
        solutions_dict["max"][0][i] = the_column.max()
        solutions_dict["min"][0][i] = the_column.min()
        solutions_dict["sum"][0][i] = the_column.sum()
        
        # Same logic as above but for rows, since the challenge asks for each column and row, easier to do in 1 loop
        # i, : gives every entry in the ith row
        the_row = matrix[i, :]
        
        solutions_dict["mean"][1][i] = the_row.mean()
        solutions_dict["variance"][1][i] = the_row.var()
        solutions_dict["standard deviation"][1][i] = the_row.std()
        solutions_dict["max"][1][i] = the_row.max()
        solutions_dict["min"][1][i] = the_row.min()
        solutions_dict["sum"][1][i] = the_row.sum()
        
    # These are for the entire matrix so no iteration/looping here
    solutions_dict["mean"][2] = matrix.mean()
    solutions_dict["variance"][2] = matrix.var()
    solutions_dict["standard deviation"][2] = matrix.std()
    solutions_dict["max"][2] = matrix.max()
    solutions_dict["min"][2] = matrix.min()
    solutions_dict["sum"][2] = matrix.sum()

    return solutions_dict

# Testing it
calculate(ex1)