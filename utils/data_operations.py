# -*- coding:utf-8 -*-
'''
Created on 2017年6月20日

@author: Thinkpad
'''
from copy import deepcopy

def flatten_list(complexlist): # [[],[]] -> []
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
    
    
def do_split(string, delimiter = ','): # passive to initiative, for using do_split(None or '',)
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
    
    
if __name__ == '__main__':
    complexlist = [[1,2],[3,4],[5,6],7,8,'abc', xrange(3)]
    print str(flatten_list(complexlist))
    
    newlist = eliminate_none_items([None, 1, None, 3])
    print newlist
    
    dictlist = [{'a':1,'b':2}, {'a':3}, {'b':3}]
    vallist = vallist_from_dictlist(dictlist, 'a')
    print vallist
    
    origlist = [1,2,3]
    newlist = list_to_tuplelist(origlist)
    print newlist

    newlist = dictlist_to_tuplelist([{'a':1,'b':2},{'c':3}])
    print newlist
    
    newlist = strip_list([' a ', ' TEST', 1, None, {'a':1,'b':2},{'c':3}, '  cc  '])
    print newlist