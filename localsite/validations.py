# -*- coding: utf-8 -*-

def is_ean(value, product=None):
    '''Check if the EAN format is Ok'''
    try:
        check = int(value)
        if len(value) == 13:
            return True, value
        else:
            return False, value
    except:
        return False, value