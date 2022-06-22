# %%
from ast import Assert
from logging import raiseExceptions
import string
from numpy import string_
import pandas as pd
import os
import json
import random


os.chdir(os.path.dirname(os.path.realpath(__file__)))
f=open(r"input.json")
input=json.load(f)
f.close()
print(type(input))
#thinking of hardcoding tiers
class var:
    def assign_from_json(key_for_json,optional_value=None):
        try:
            return input[key_for_json]
        except KeyError:
            if optional_value!=None:
                return optional_value
            else:
                raiseExceptions(key_for_json, ": Required Input not found")


    equip=assign_from_json("equip")

    Tiers= ("Rare", "Epic", "Unique", "Legend")
    main_line=assign_from_json("main_line")
    assert main_line!="Rare", "This spreadsheet doesn't suppport Rare cubing"
    assert main_line in Tiers, "Main Line is not recognised"
    sub_line=Tiers[Tiers.index(main_line)-1]

    desired_lines=tuple(assign_from_json("desired_lines"))
    desired_number=assign_from_json("desired_number")

    additional=assign_from_json("additional")
    cube_name=assign_from_json("cube_name")
    if cube_name!='':
        df=pd.read_csv("Resources/prime rates.csv", index_col=0, na_values='')
        x=df.loc[:,main_line][cube_name]
        assert x!='-', "can't cube {0} equip with {1} cube".format(main_line,cube_name)
        prime_rates=tuple(map(float, x.split(',')))
    else:
        prime_rates=tuple(assign_from_json("prime_rates"))
    print("Prime rates of cubes are: ",prime_rates)

    csv_header= [] # ["line1", "line2", "line3",...,"desired"]
    for x in range(len(prime_rates)):
        csv_header.append("Line "+ str(x+1))
    csv_header.append("desired")

    sample_size=assign_from_json("sample_size", 10000)
    Lines={}

del f, input

class cube: #probably making a child from this
    def read_csv():
        for i in (var.main_line,var.sub_line):
            try:
                var.Lines[i]=pd.read_csv("Resources/{0}/{1}{2}.csv".format(var.equip,"Add_" if var.additional else "" ,i))
            except FileNotFoundError:
                raiseExceptions("No records for",i, var.equip,)
    
    def show_lines():
        for x in var.Lines.items():
            print(x[0]) #rank
            print(list(x[1].Line)) #lines
            print()



#probably puting this part into cube class
def roll_lines(prime_rate):
    equip_line=[]
    for i in prime_rate:
        if random.randint(1, 1000000)<=int(i*10000):
            equip_line+=random.choices(list(var.Lines[var.main_line].Line), weights=tuple(var.Lines[var.main_line].Weight), k=1)# generate main line
        else:
            equip_line+=random.choices(list(var.Lines[var.sub_line].Line), weights=tuple(var.Lines[var.sub_line].Weight), k=1)# generate secondary line
    return equip_line

#to reject line i probably need a method to count lines

cube.read_csv()
cube.show_lines()
"""hard coding reject class for now"""
class reject:
    all=[]
    count=0
    def __init__(self,string_to_reject, lines,identifier=None):
        self.string_to_reject=string_to_reject
        self.lines=lines
        self.identifier=identifier
        all.append(self)
        count+=1
    def check(list):
        pass #return boolean true if pass and false if fail 

test_lines=["STR", "STR","STR"]
Decent=reject("Decent",1,"Decent skills")
Decent.check(test_lines)

"""Test cubes"""
df=[] #df represent the full data
for x in range(var.sample_size): 
    result=roll_lines(var.prime_rates) #result is a list
    """
    implement rejects here
    """
    i=0
    for y in result: #y is a string
            if y.startswith(var.desired_lines):
                i+=1
    result.append(i)
    df.append(result)
del x,y
df=pd.DataFrame(df,columns=var.csv_header) 
# df1=df[df.line1.str.startswith("C")]
df1=df[df.desired>=var.desired_number]
df.to_csv(r'all lines.csv')
df1.to_csv(r"desired.csv")


print("Total cubes: ", df.shape[0])
print("Desired lines: ", df1.shape[0])
print("Success Chance: ", df1.shape[0]/df.shape[0]*100,"%")





