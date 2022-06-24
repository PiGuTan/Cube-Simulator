# %%
from logging import raiseExceptions
import re
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

class cube_lines_weight: #probably making a child from this
    def __init__(self,line):
        try:
            df=pd.read_csv("Resources/{0}/{1}{2}.csv".format(var.equip,"Add_" if var.additional else "" ,line))
        except FileNotFoundError:
            raiseExceptions("No records for",var.main_line, var.equip,)

        self.possible_lines=list(df.Line)
        self.weight=tuple(df.Weight)

    def show_lines(self):
#!!!! change this and put this into variables
        print(self.possible_lines)

main_lines=cube_lines_weight(var.main_line)
sub_lines=cube_lines_weight(var.sub_line)



#to reject line i probably need a method to count lines

main_lines.show_lines()
sub_lines.show_lines()
"""hard coding reject class for now"""
class reject:
    all=[]
    count=0
    def check(self,list): 
        match_lines=0
        for x in list:
            if re.match(self.string_to_reject,x):
                match_lines+=1
        return match_lines
    def __init__(self,string_to_reject, lines,identifier=None):
        self.string_to_reject=string_to_reject
        self.lines=lines
        self.identifier=identifier
        if (self.check(main_lines.possible_lines)>0 or self.check(sub_lines.possible_lines)>0): #issue here always true
            reject.all.append(self)
            reject.count+=1

    def check_all(cube_results):
        for x in reject.all:
            if x.check(cube_results)>x.lines:
                return False
        return True

#probably puting this part into cube class
def roll_once(prime_rate):
    equip_line=[]
    for i in prime_rate:
        if random.randint(1, 1000000)<=int(i*10000):
            #!! var.Lines[var.main_line].Line this will not work
            equip_line+=random.choices(main_lines.possible_lines, weights=main_lines.weight, k=1)# generate main line
        else:
            equip_line+=random.choices(sub_lines.possible_lines, weights=sub_lines.weight, k=1)# generate secondary line
    return equip_line

def roll_lines(prime_rates):
    roll=roll_once(prime_rates)
    while True:
        if not reject.check_all(roll):
            roll=roll_once(prime_rates)
        else:
            return roll



"""
    def check_all(list):
        current=True
        for x in reject.all:
            current=current & x.check(list)
        return current
"""

test_lines=["Decent sharp eyes enabled", "Decent speed infusion enabled","STR","Damage when attacking boss monsters +20%", "Damage when attacking boss monsters +20%"]
Decent=reject("Decent .* enabled",1,"Decent skills")
Invincibility_Time=reject("Invincibility time \+[0-9] second when hit", 1, "Invincibility time")
IED=reject("Ignore Enemy Defense \+[0-9]{1,2}%",2,"Ignore Enemy Defense %")
Ignore_Damage_On_Hit=reject("[0-9]{1,2}% chance to ignore 40% damage when hit",2,"Damage Reduction")
Invincibility_Chance=reject("[0-9]% chance of being invincible for 7 seconds when hit",2,"Invincibility cahnce on hit")
Item_Drop_Rate=reject("Item Drop Rate \+[0-9]{1,2}%", 2,"Item Drop")
Boss_Damage=reject("Damage when attacking boss monsters \+[0-9]{1,2}%", 2,"BD")
print(Decent.check(test_lines)) #need debug this
print(IED.check(test_lines))
print(Ignore_Damage_On_Hit.check(test_lines))
print(Invincibility_Chance.check(test_lines))
print(Item_Drop_Rate.check(test_lines))
print(Boss_Damage.check(test_lines))
print("Last print")
print(len(reject.all))
print(reject.count)
for x in reject.all:
    print(x.string_to_reject)
print()
#print(reject.check_all(test_lines))

"""Test cubes"""
df=[] #df represent the full data
for x in range(var.sample_size): 
    result=roll_lines(var.prime_rates) #result is a list
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





