import pandas as pd

class cube:
    def __init__(cube_type,line="Legend", primerate=(100,.2,.2)):
        cube_type.line=line
        cube_type.primerate=primerate



df=pd.read_csv("Cube Simulator\Cube-Simulator\Resources\prime rates.csv", index_col=0)
#df.Legend["Red"] # referebce a cell

df.Legend["Red"]

df.loc[:,"Epic"]["Purple"]

tuple(map(float, df.loc[:,"Epic"]["Purple"].split(',')))

import os
subfolders = ["Belt","Bottom","Cape","Earring","Emblem","Eye","Face","Glove","Hat","Heart","Pendant","Ring","Secondary","Shoe","Shoulder","Template","Top","Weapon"]
path_of_the_directory= r"C:/Users/pigut\Desktop/Projects/Cube Simulator/Cube-Simulator/Resources"
def printfiles(directory_path):
    for filename in os.listdir(directory_path):
        f = os.path.join(directory_path,filename)
        if os.path.isfile(f):
            print(f)
        else: #folder
            print(filename)
for i in subfolders:
    printfiles(path_of_the_directory+"/"+i)