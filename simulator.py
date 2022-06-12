# %%
import pandas as pd

equip=r"Weapon"
cube_name="Additional" #leave it as a blank string if you are lanning to input prime_rates
prime_rates=(100,00,0) # Can put None if cube_name and main_line is given
desired_lines=("ATT")
desired_number=2
main_line="Legend" # "Epic", "Unique", "Legend"
additional = True
column_header= [] # ["line1", "line2", "line3",...,"desired"]
for x in range(len(prime_rates)):
    column_header.append("line"+ str(x+1))
column_header.append("desired")
Tiers= ("Rare", "Epic", "Unique", "Legend")
sub_line=Tiers[Tiers.index(main_line)-1]
Lines={}

if cube_name!='':
    # can use this to get file path 
    # os.path.dirname(os.path.realpath(__file__))
    df=pd.read_csv("Resources/prime rates.csv", index_col=0, na_values='')
    x=df.loc[:,main_line][cube_name]
    assert x!='-', "can't cube {0} equip with {1} cube".format(main_line,cube_name)
    prime_rates=tuple(map(float, x.split(',')))
    print(prime_rates)


"""
Checking the dataframe in Lines
"""
for i in (main_line,sub_line):
    try:
        Lines[i]=pd.read_csv("Resources/{0}/{1}{2}.csv".format(equip,"Add_" if additional else "" ,i))
    except FileNotFoundError:
        print("No records for",i, equip,)
print(Lines[sub_line].shape) # shows all number of lines
print(Lines[main_line].shape)


"""
printing possible lines
"""
for x in Lines.items():
    print(x[0])
    print(list(x[1].Line))


import random


def cube(prime_rate):
    equip_line=[]
    for i in prime_rate:
        if random.randint(1, 1000000)<=int(i*10000):
            equip_line+=random.choices(list(Lines[main_line].Line), weights=tuple(Lines[main_line].Weight), k=1)# generate main line
        else:
            equip_line+=random.choices(list(Lines[sub_line].Line), weights=tuple(Lines[sub_line].Weight), k=1)# generate secondary line
    return equip_line

"""Test cubes"""
df=[] #df represent the full data
for x in range(100000): 
    result=cube(prime_rates) #result is a list
    i=0
    for y in result: #y is a string
            if y.startswith(desired_lines):
                i+=1
    result.append(i)
    df.append(result)
del x,y
df=pd.DataFrame(df,columns=column_header) 
# df1=df[df.line1.str.startswith("C")]
df1=df[df.desired>=desired_number]
df.to_csv(r'all lines.csv')
df1.to_csv(r"desired.csv")


print(df.shape)
print(df1.shape)
print(df1.shape[0]/df.shape[0]*100,"%")





