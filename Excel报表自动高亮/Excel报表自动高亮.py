# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:27:37 2020

@author: wyx
"""


import xlrd,xlwt
from xlutils.copy import copy
data=xlrd.open_workbook('./楼宇安防.xls',formatting_info=True)
workbook=xlwt.Workbook(encoding='utf-8')
workbook=copy(data)
tableRead=data.sheet_by_index(0)
tableWrite=workbook.get_sheet(0)

#设置高亮
style=xlwt.XFStyle()
pattern=xlwt.Pattern()
pattern.pattern=xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour=xlwt.Style.colour_map['yellow']
style.pattern=pattern

#高亮数据
col_index=tableRead.row_values(0).index('体温')
for i in range(1,tableRead.nrows):
    temp=tableRead.cell_value(i,col_index)
    if temp>37.4:
        tableWrite.write(i,col_index,temp,style)

#写入平均体温
tableWrite.write(tableRead.nrows,0,'平均体温')
tableWrite.write(tableRead.nrows,
                 col_index,
                 sum(tableRead.col_values(col_index,
                                          start_rowx=1,
                                          end_rowx=None))/tableRead.nrows-1)

#保存数据
workbook.save('./作业.xls')
