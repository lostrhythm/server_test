# -*- coding:utf-8 -*-
'''
Created on 2017年6月20日

@author: Thinkpad
'''
from copy import deepcopy

def flatten_list(complexlist): 
    plainlist = []
    for i in complexlist:
        if i.__class__ in [list().__class__, set().__class__, dict().__class__]:
            plainlist.extend(i)
        else:
            plainlist.append(i)
        
    return plainlist
    


def eliminate_none_items(origlist):
    newlist = deepcopy(origlist)
    
    for i in origlist:
        if i == None:
            newlist.remove(i)
            
    return newlist
    
    
def eliminate_placeholders(origlist):
    newlist = deepcopy(origlist)
    
    for i in origlist:
        if i == 'placeholder':
            newlist.remove(i)
            
    return newlist
    
def vallist_from_dictlist(dictlist, aimkey, eli_none = True):
    vallist = []
    for d in dictlist:
        vallist.append(d.get(aimkey))
        
    if eli_none:
        vallist = eliminate_none_items(vallist)
    else:
        pass
    
    return vallist
    
    
def do_split(string, delimiter = ','): 
    if string:
        retlist = string.split(delimiter)
    else:
        retlist = []
    return retlist


def list_to_tuplelist(origlist):
    newlist = []
    for i in origlist:
        newlist.append((i,))
        
    return newlist
    
    
def safe_remove(origlist, item):
    try:
        origlist.remove(item)
    except:
        pass
    return origlist


def dictlist_to_tuplelist(dictlist):
    newlist = []
    for _dict in dictlist:
        newlist.append( tuple(_dict.values()) )
    
    return newlist

def strip_list(origlist):
    newlist = []
    for i in origlist:
        try:
            newlist.append(i.strip())
        except:
            newlist.append(i)
            
    return newlist
    
    
    
def _add(x,y):
    try:
        ret = x + y
    except:
        ret = {}
        for k in x:
            ret[k] = x[k] + y[k]
            
    return ret
      
def general_add(objects_list):
    return reduce(_add, objects_list)
    
def row_add(matrix_dict):
    AllRowSum_dict = {}
    for RowKey in matrix_dict:
        row_dict = matrix_dict[RowKey]
        
        rowvalue_list = []
        for ColumnKey in row_dict:
            rowvalue_list.append(row_dict[ColumnKey])
            
        AllRowSum_dict[RowKey] = general_add(rowvalue_list)

    return AllRowSum_dict
    
    
def trans(matrix_dict):
    matrix_t_dict = {}
    for RowKey in matrix_dict:
        row_dict = matrix_dict[RowKey]
        
        for ColumnKey in row_dict:
            if not matrix_t_dict.has_key(ColumnKey):
                matrix_t_dict[ColumnKey] = {} 
                
            matrix_t_dict[ColumnKey][RowKey] = row_dict[ColumnKey]
        
    return matrix_t_dict
    
    
def column_add(matrix_dict):
    matrix_t_dict = trans(matrix_dict)
    return row_add(matrix_t_dict)
    

    
    
    
if __name__ == '__main__':
#     complexlist = [[1,2],[3,4],[5,6],7,8,'abc', xrange(3)]
#     print str(flatten_list(complexlist))
#     
#     newlist = eliminate_none_items([None, 1, None, 3])
#     print newlist
#     
#     dictlist = [{'a':1,'b':2}, {'a':3}, {'b':3}]
#     vallist = vallist_from_dictlist(dictlist, 'a')
#     print vallist
#     
#     origlist = [1,2,3]
#     newlist = list_to_tuplelist(origlist)
#     print newlist
# 
#     newlist = dictlist_to_tuplelist([{'a':1,'b':2},{'c':3}])
#     print newlist
#     
#     newlist = strip_list([' a ', ' TEST', 1, None, {'a':1,'b':2},{'c':3}, '  cc  '])
#     print newlist
    
    
    
    from collections import Counter
    
    l1 = Counter({'a':1,'b':2})
    l2 = Counter({'a':1,'b':2})
    print general_add([l1,l2])
    
    matrix_dict = {
                   'r1':{'c1':{'t1':1, 't2':1}, 'c2':{'t1':2, 't2':2}},
                   'r2':{'c1':{'t1':3, 't2':3}, 'c2':{'t1':4, 't2':4}}
                    
                   }
    print row_add(matrix_dict)
    print trans(matrix_dict)
    print column_add(matrix_dict)
    
    

    