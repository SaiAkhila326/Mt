import ctypes
import numpy as np

# Step 1: Load the shared object (op.so) file
example = ctypes.CDLL('/home/sai-akhila/Desktop/q1m/codes/op.so')

# Step 2: Define the argument types and return types for the required C functions
example.Matscale.argtypes = [
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int, ctypes.c_double
]
example.Matscale.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

example.Matadd.argtypes = [
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int
]
example.Matadd.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

example.Matsec.argtypes = [
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_double
]
example.Matsec.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

# Step 3: Helper function to convert a numpy array into a ctypes 2D array
def create_2d_array(arr):
    arr_ctypes = (ctypes.POINTER(ctypes.c_double) * arr.shape[0])()
    for i in range(arr.shape[0]):
        arr_ctypes[i] = arr[i].ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    return arr_ctypes

# Step 4: Define input arrays 'a' and 'b' (2x1 matrices)
a = np.array([[1], [2]], dtype=np.float64)  # Vector a: [[1], [2]]
b = np.array([[3], [4]], dtype=np.float64)  # Vector b: [[3], [4]]
m = 2                                       # Number of rows in a and b
n = 1                                       # Columns in vectors (1-column vectors)
k = 3.0                                     # Scalar for Matsec function

# Convert the numpy arrays into ctypes arrays
a_ctypes = create_2d_array(a)
b_ctypes = create_2d_array(b)

# Step 5: Create vectors A = 2a - 3b and B = a + b using Matscale and Matadd

# A = 2a - 3b
scaled_a_2 = example.Matscale(a_ctypes, m, n, 2.0)  # 2a
scaled_b_3 = example.Matscale(b_ctypes, m, n, -3.0) # -3b
A_ctypes = example.Matadd(scaled_a_2, scaled_b_3, m, n)  # A = 2a - 3b

# B = a + b
B_ctypes = example.Matadd(a_ctypes, b_ctypes, m, n)  # B = a + b

# Step 6: Call the C function Matsec on A and B
result_ctypes = example.Matsec(A_ctypes, B_ctypes, m, k)

# Step 7: Convert the result back to a numpy array for easier handling
result_np = np.zeros((m, 1), dtype=np.float64)
for i in range(m):
    result_np[i][0] = result_ctypes[i][0]

# Step 8: Generate LaTeX Table

def array_to_latex_row(arr):
    return " & ".join(map(lambda x: f"{x:.2f}", arr)) + " \\\\"

latex_table = r"""
\documentclass{article}
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{array}
\begin{document}

\begin{table}[h!]
\centering
\begin{tabular}{|c|c|c|c|c|c|}
\hline
\textbf{Row} & \textbf{a} & \textbf{b} & \textbf{A = 2a - 3b} & \textbf{B = a + b} & \textbf{Resultant Vector} \\
\hline
"""

for i in range(m):
    latex_table += f"Row {i+1} & {a[i][0]:.2f} & {b[i][0]:.2f} & {A_ctypes[i][0]:.2f} & {B_ctypes[i][0]:.2f} & {result_np[i][0]:.2f} \\\\\n"

latex_table += r"""
\hline
\end{tabular}
\caption{Vectors a, b, A, B, and Result from Matsec function}
\end{table}

\end{document}
"""

# Step 9: Write LaTeX table to a .tex file
with open('output_table.tex', 'w') as f:
    f.write(latex_table)

print("LaTeX table written to output_table.tex")

