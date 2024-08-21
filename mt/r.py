import sympy as sp
import numpy as np
#Code by GVV Sharma
#September 12, 2023
#Revised July 21, 2024
#released under GNU GPL
#Point Vectors


import sys                                          #for path to external scripts
sys.path.insert(0, '/home/sai-akhila/Desktop/p/matgeo/codes/CoordGeo')        #path to my scripts
import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#local imports
from line.funcs import *
from triangle.funcs import *
from conics.funcs import circ_gen


#if using termux
#import subprocess
#import shlex
#end if
P = np.array(([-1, 3])).reshape(-1,1) 
Q = np.array(([2, 5])).reshape(-1,1)  

R=((3/2)*Q+P)/(5/2)

print(R)



#Generating all lines
x_PQ = line_gen(P,Q)
x_PR = line_gen(P,R)

#Plotting all lines
plt.plot(x_PQ[0,:],x_PQ[1,:],label='$PQ$')
plt.plot(x_PR[0,:],x_PR[1,:],label='$PR$')

#Labeling the coordinates
tri_coords = np.block([[P,Q,R]])
plt.scatter(tri_coords[0,:], tri_coords[1,:])
vert_labels = ['A','B','O']
for i, txt in enumerate(vert_labels):
    #plt.annotate(txt, # this is the text
    plt.annotate(f'{txt}\n({tri_coords[0,i]:.0f}, {tri_coords[1,i]:.0f})',
                 (tri_coords[0,i], tri_coords[1,i]), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(20,5), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center

# use set_position
ax = plt.gca()
ax.spines['top'].set_color('none')
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
#plt.xlabel('$x$')
#plt.ylabel('$y$')
plt.legend(loc='best')
plt.grid() # minor
plt.axis('equal')

#if using termux
#plt.savefig('chapters/10/7/1/7/figs/fig.pdf')
#subprocess.run(shlex.split("termux-open chapters/10/7/1/7/figs/fig.pdf"))
#else
plt.show()
