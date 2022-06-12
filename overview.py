import pandas as pd

class cube:
    def __init__(cube_type,line="Legend", primerate=(100,.2,.2)):
        cube_type.line=line
        cube_type.primerate=primerate

import os
subfolders = ["Belt","Bottom","Cape","Earring","Emblem","Eye","Face","Glove","Hat","Heart","Pendant","Ring","Secondary","Shoe","Shoulder","Template","Top","Weapon"]
current_directory = os.path.dirname(os.path.realpath(__file__))
resource_directory=current_directory + r"/Resources"

def collate_csv(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path,filename)
        if os.path.isfile(file_path) & file_path.endswith(r".csv"):
            print(file_path)
            pass

for i in subfolders:
    collate_csv(resource_directory+"/"+i)


"""
df=pd.read_csv("\Resources\prime rates.csv", index_col=0)
#df.Legend["Red"] # referebce a cell

df.Legend["Red"]

df.loc[:,"Epic"]["Purple"]

tuple(map(float, df.loc[:,"Epic"]["Purple"].split(',')))
"""
