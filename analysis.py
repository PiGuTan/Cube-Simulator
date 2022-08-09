# %%
import os
import sys
import pandas as pd
import json
import numpy as np

#import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

os.chdir(sys.path[0])
f=open(r"analysis_input.json")
input=json.load(f)
f.close()
f=open(r"input.json")
settings=json.load(f)
f.close()
df=pd.read_csv("Desired.csv", index_col=0, na_values='')

# %%
sample_size=settings["sample_size"]

# %%

class keep:
    all=[]
    def __init__(self,name, before='', after=''):
        self.name=name
        self.before=before
        self.after=after
        self.df=pd.DataFrame({})
        keep.all.append(self)
    def init_df(self,df,column_header,number):
        self.df[self.name+' '+str(number)]=df[column_header].apply(lambda x:self.get_value(x))
        if len(df.keys())>3:
            self.summary=self.df.apply(keep.top3_edit, axis=1)
        else:
            self.summary=self.df.sum(axis=1)
        self.summary.name=self.name
    def inside(self, string):
        if string.endswith(self.after) and string.startswith(self.before):
            return True
        else:
            return False
    def get_value(self, string):
        if self.inside(string):
            x=string.replace(self.before,"",1)
            x=x.removesuffix(self.after)
            return int(x)
        else: return 0 # maybe changing to  return none
    def top3_edit(row):
        temp_list=row[row.keys()].values.tolist()   
        temp_list= list(filter(lambda num:num>0,temp_list))
        if len(temp_list)>3:
            temp_list.sort(reverse=True)
            return sum(temp_list[0:3])
        else:
            return sum(temp_list)
    def inside_all(string):
        for x in keep.all:
            if x.inside(string):
                return True
        return False
before=0
after=1
keep_dict={}
for x in input.keys():
    keep_dict[x]=keep(x,input[x][before],input[x][after])
del before, after, input
#theres 2 collections keep_dict and keep.list


# %%
header=df.keys()
header=list(filter(lambda x: x.startswith("Line "),header))

# %%
count=0
for x in header:
    count+=1
    df[x]=df[x].apply(lambda x: x if keep.inside_all(x) else '')
    for y in keep.all:
        y.init_df(df,x,count)
for x in keep.all:
    df[x.name]=x.summary


# %%
df.to_csv("analysed.csv")

# %%
def generate_graph(keep_object):
    new_df=keep_object.summary
    x_axis = list(set(new_df.unique()))
    x_axis.sort()
    y_axis=[0]
    for x in x_axis:
        if x ==0:
            continue
        y_axis.append(new_df[new_df==x].count())
    z_axis=list(np.cumsum(y_axis[::-1]))[::-1]
    x_title=keep_object.name + " with " + str(sample_size) + " samples"
    y_title="Count of samples with " +keep_object.name +" equal to" 
    z_title="Total samples with " + keep_object.name + " greater than"
    z_axis[0]=sample_size
    y_axis[0]=sample_size-sum(y_axis)

    fig = make_subplots(rows=2, cols=1, row_heights=[.85,.15], shared_xaxes=True)

    bar_chart = go.Bar(x=x_axis,y=y_axis, name=y_title, text=y_axis)
    fig.add_trace(bar_chart, row=1,col=1)

    cum_chart = go.Scatter(x=x_axis,y=z_axis, name=z_title)
    fig.append_trace(cum_chart, row=1,col=1)

    box_plot=go.Box(x=new_df[new_df!=0], notched=True, name="Boxplot")
    fig.add_trace(box_plot, row=2, col=1)
    fig.update_layout(title_text=x_title)
    fig.write_html('output/'+ keep_object.name+'.html', auto_open=False)
    fig.show()

# %%
generate_graph(keep.all[0])


# %%
generate_graph(keep.all[1])

# %%
generate_graph(keep.all[2])

# %%



