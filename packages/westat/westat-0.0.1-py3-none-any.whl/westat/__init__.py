import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
mpl.rcParams['font.family'] = 'SimHei'        #设置中文字体

from pandas import read_csv,read_excel
from westat.LogisticScoreCard import *


def tree_img(file_name,path = '',type = 'svg'):
    # 修改字体为中文
    file_txt= ''
    with open(file_name,'r',encoding='utf-8') as f:
        for line in f:
            line = line.replace('helvetica','SimHei')
            file_txt = file_txt + line
        
    with open(file_name,'w',encoding='utf-8') as f:
        f.write(file_txt)

    # 转换决策树到图片 
    if path:
        file_path = path
    else:
        file_path = os.path.splitext(file_name)[0] + '.' + type

    str_exec = 'dot -T' + type + ' ' + file_name + ' -o ' + file_path   # 决策树转图片命令  
    print(str_exec)
    result = os.popen(str_exec)
    return result

def tree_pdf(file_name,path=''):
    # 修改字体为中文
    file_txt= ''
    with open(file_name,'r',encoding='utf-8') as f:
        for line in f:
            line = line.replace('helvetica','SimHei')
            file_txt = file_txt + line
        
    with open(file_name,'w',encoding='utf-8') as f:
        f.write(file_txt)

    # 转换决策树到图片 pdf文件
    if path:
        file_path = path
    else:
        file_path = os.path.splitext(file_name)[0] + '.pdf'

    str_exec = 'dot -Tpdf ' + file_name + ' -o ' + file_path   # 决策树转pdf命令
    print(str_exec)
    result = os.popen(str_exec)
    return result


class Table(pd.DataFrame):
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return 'table for westat'
    


        
        