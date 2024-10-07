import numpy as np

# Step 1: Read the vectors from output.txt (vertically)
def read_vectors_from_file(output):
    with open(output, 'r') as file:
        lines = file.readlines()
        # Split the lines into numbers and create a 2D list
        matrix = [list(map(float, line.split())) for line in lines]
        # Convert this into a NumPy array and then transpose to get columns as vectors
        matrix = np.array(matrix).T  # Transpose the matrix to switch rows and columns
        vector1 = matrix[0]  # First vector (first column after transpose)
        vector2 = matrix[1]  # Second vector (second column after transpose)
    return vector1, vector2

# Step 2: Multiply the first vector by 5/4 and write to LaTeX file
def write_latex_table(filename, vector1, scaled_vector, vector2):
    with open(filename, 'w') as file:
        file.write("\\begin{tabular}{|c|c|c|}\n")
        file.write("\\hline\n")
        file.write("Original $a$ & Vector obtained after applying section formula $\\frac{5}{4}a$ & Verification \\\\ \n")
        file.write("\\hline\n")
        for i in range(len(vector1)):
            file.write(f"{vector1[i]:.4f} & {scaled_vector[i]:.4f} & {'True' if np.isclose(scaled_vector[i], vector2[i]) else 'False'} \\\\ \n")
        file.write("\\hline\n")
        file.write("\\end{tabular}\n")

if __name__ == "__main__":
    # Read vectors from output.txt
    vector1, vector2 = read_vectors_from_file('output.txt')
    
    # Multiply the first vector by 5/4
    scaled_vector1 = vector1 * 5/4
    
    # Write the results to a .tex file
    write_latex_table('output_table.tex', vector1, scaled_vector1, vector2)
    
    #print("LaTeX table written to 'output_table.tex'")

