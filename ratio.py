
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

I = np.eye((2))
e1 = I[:,0].reshape(-1, 1)
#Given points
A = np.array(([-6, 0])).reshape(-1,1) 
B = np.array(([3, -8])).reshape(-1,1)  
C = np.array(([-4, 6])).reshape(-1,1)
#Equidistant point


# Distances
d1= LA.norm(A-C)
d2= LA.norm(B-C)
print(d1/d2)

#Generating all lines
x_AC = line_gen(A,C)
x_CB = line_gen(C,B)

#Plotting all lines
plt.plot(x_AC[0,:],x_AC[1,:],label='$AC$')
plt.plot(x_CB[0,:],x_CB[1,:],label='$CB$')

#Labeling the coordinates
tri_coords = np.block([[A,B,C]])
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
