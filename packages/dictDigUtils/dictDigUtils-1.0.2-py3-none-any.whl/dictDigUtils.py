#!/usr/bin/env python
""" simple utility functoins to handle dicts
"""

def dict_flatten(d: dict, root_key: str ='' , sep: str ='/')->dict:
    """ Flatten a dict key tree in place (use the same dict
        in the process)

        @parameter d dict
        @parameter root_key a string of actual root
        @parameter sep string a separator character

        @result a dict with flattened keys
    """

    if not isinstance(d, dict):
        raise TypeError('d must be a dict!')
    klist = list(d.keys())
    for k in klist:
        if root_key != '':
            newkey = f'{root_key}{sep}{k}'
            d[newkey] = d.pop(k)
            k = newkey

        if isinstance(d[k], dict):
            d.update(dict_flatten(d.pop(k), k))
    return d
# end of dict_flatten


def dict_key_cut(di: dict, sep: str ='/', level: int =2, ignore_char: str =None) ->dict:
    """ truncate flat dict keys to a specific level in place
        (use the same dict in the process)
        @parameter d dict
        @parameter sep string separator in key
        @parameter level integer maximum level
        @parameter ignorechar string, skip keys containing this string

        @return result dict
    """

    if not isinstance(d, dict):
        raise TypeError('d must be a dict')

    klist = list(d.keys())
    for k in klist:
        if ignore_char is not None and ignore_char in k:
            continue

        kl = k.rsplit(sep, level)
        if len(kl) == (level+1):
            d[sep.join(kl[1:])] = d.pop(k)

    return(d)
# end of dict_key_cut


def dict_disp(d: dict, level: int =0)->None:
    """ Take a dict, and go through its keys and values, display them in a
        tabulated form.
        Run recursively for dicts inside

        @param d        dict to be displayed
        @param level    level of indentation we are at

        return: nothing
    """
    mtabs = '\u2014\u2014'*level if level > 0 else ''
    mtabs = f'{level}{mtabs}'
    tabs = '  '*level if level > 0 else ''
    tabs = f' {tabs}'

    if type(d) != dict:
        raise ValueError('Invalid input variable type!')
        return

    firstLine= True
    for k,v in d.items():
        if firstLine:
            spacer= f'\u251C{mtabs}>'
            firstLine= False

        else:
            spacer = f'\u2502{tabs} '

        if type(v) == dict:
            print(f'{spacer} {k}:')
            dict_disp(v, level= level+1)
        else:
            print(f'{spacer} {k}: ({type(v).__name__}) {v}')

    if level > 0:
        print('\u2502')
    else:
        print('')
# end of dict_disp


def dict_search_in_key(search: str,  data: dict)->list:
    """ Run a search in the keys such that the search text should be
        part of the last key to obtain a return value.
        This function recursively walks the dict tree for the search.

        For example, for a dict with elements:
        {key1: {key2: {key3: 1}}}
        returns for search 'key2': [{key3:1}]
        for search 'key3' returns [1]

        @param search   the search text
        @param data     the dict searching in

        @return         a list of found dict elements, without their key.
    """
    if not isinstance(search, str) or not isinstance(data, dict):
        raise ValueError('inproper input type')

    res = []
    for k,v in data.items():
        if ((isinstance(k, str) and search in k)
            or k == search):
            res.append(v)
        elif isinstance(v, dict):
            newres = dict_search_in_key(search, v)

            if newres:
                res += newres
        elif isinstance(v, list):
            for i in v:
                if isinstance(i, dict):
                    newres = dict_search_in_key(search, i)
                    if newres:
                        res += newres
    # end of for in data
    return res
# end of search_in_dict


def dict_list_keys(data: dict)->list:
    """ recursively list up all keys of a dict
    """
    res = list(data.keys())

    for k,v in data.items():
        if isinstance(v, dict):
            res_line = dict_list_keys(v)
            if res_line:
                res += res_line
    if res:
        # make the results unique
        return list(set(res))
    else:
        return []
# end of dict_list_keys
