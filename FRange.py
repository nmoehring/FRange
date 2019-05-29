#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frange.py
Created on Sat May 25 18:21:57 2019
@author: nathan

A float-range class that handles unions and intersections. Created primarily to 
track the domains of functions.

Arguments in form of iterables of iterables, like [[lower,upper,'[)']]
        [lower,upper)

Has a rand() method which returns a random number within the object's range.
"""

import pdb
from random import random

class FRange:
    def __init__(self, float_range, step=0.5):
        self._step = step
        self._rg = []
        self.union(float_range)
        
    def union(self, float_range):
        ''' Adds the range in the argument to the ranges in the object
         Joins ranges that are touching or overlapping '''
        rg_arg = self._get_std_arg(float_range)
        for rg in rg_arg:
            self._rg.append(rg)
        self._cleanup()
            
    def intersect(self, float_range):
        ''' Keeps the range of the object that coincides with argument range'''
        rg_arg = self._get_std_arg(float_range)
        idxs_to_keep = []
        for rg in rg_arg:
            idxs = self._check_intersections(rg)
            idxs_to_keep += list(range(idxs[0],idxs[-1]+1))
            if len(idxs) > 2: idxs = [idxs[0],idxs[-1]]
            if len(idxs) != 0:
                self._rg[idxs[0]] = self._get_intersection(self._rg[idxs[0]], rg)
                if len(idxs) == 2:
                    self._rg[idxs[1]] = self._get_intersection(self._rg[idxs[1]], rg)
        for i in reversed(range(len(self._rg))):
           if i not in idxs_to_keep: self._rg.pop(i) 
        self._cleanup()
               
    def _check_intersections(self, limits):
        ''' Checks if the range in the argument intersects a range in the object'''
        return [i for i in range(len(self._rg)) if 
             self._rg[i][0] <= limits[0] <= self._rg[i][1] or
             self._rg[i][0] <= limits[1] <= self._rg[i][1] or
             (limits[0] < self._rg[i][0] and limits[1] > self._rg[i][1])]
            
    def _get_std_arg(self,float_range):
        ''' Creates a list of lists or tuples, if necessary '''
        # Prioritizing input in interval notation
        if type(float_range) == str:
            if self._isValidStr(float_range):
                return self._convertStr([float_range]) 
            else: 
                raise TypeError("Incorrect range format")
                
        #For catching problems with input or identifying the format of the input
        not_iters = True
        value_spotted = False
        all_strings = True
        valid_strings = True
        
        for element in float_range:
            if type(element) in (list,tuple):
                not_iters = False
                if value_spotted:
                    raise TypeError("Incorrect range format.")
                all_strings = False
            elif type(element) == str:
                if not self._isValidStr(element):
                    valid_strings = False
            else:
                value_spotted = True
                if not_iters == False:
                    raise TypeError("Incorrect range format.")
                all_strings = False
        if not_iters:
            return [float_range]
        elif all_strings:
            if not valid_strings:
                raise TypeError("Incorrect range format.")
            else:
                return self._convertStr(float_range)
        else:
            return float_range
        
    def _convertStr(self, float_range):
        '''Convert string argument to standard FRange format'''
        std_list = []
        for element in float_range:
            brackets = element[0] + element[-1]
            split_str = element.split(",")
            std_list.append(([int(split_str[0][1:])] + [int(split_str[1][:-1])] + [brackets]))
        return std_list
    
    def _isValidStr(self, range_str):
        '''Check if string has valid range format'''
        if range_str[0] not in ["(","["] or range_str[-1] not in [")","]"] or range_str.find(",") == -1:
            return False
        else:
            return True
    
    def _cleanup(self):
        ''' Combines ranges belonging to the object, when possible '''
        idxs_to_remove = []
        for i in range(len(self._rg)-1):
            for j in range(i+1,len(self._rg)):
                rgs = [self._rg[i], self._rg[j]]
                rgs.sort(key=lambda x : x[0])
                if rgs[1][1] < rgs[0][1]:
                    idxs_to_remove.append(i)
                    idxs_to_remove.append(j)
                    self._rg.append(rgs[1])
                elif rgs[0][1] == rgs[1][0]:
                    if not (rgs[0][2][1] == ")" and rgs[1][2][0] == "("):
                        idxs_to_remove.append(i)
                        idxs_to_remove.append(j)
                        self._rg.append((rgs[0][0], rgs[1][1], rgs[0][2][0] + rgs[1][2][1]))
                elif rgs[0][0] == rgs[1][0]:
                    idxs_to_remove.append(i)
                    idxs_to_remove.append(j)
                    brackets = ""
                    if (rgs[0][2][0] == rgs[1][2][0] and rgs[0][2][0] == "[") or rgs[0][2][0] != rgs[1][2][0]:
                        brackets += "["
                    else:
                        brackets += "("
                    if rgs[0][1] > rgs[1][1] or (rgs[0][1] == rgs[1][1] and rgs[0][1] == ']'):
                        brackets += rgs[0][2][1]
                        t = type(rgs[0])
                        self._rg.append((rgs[0][:2] + t([brackets])))
                    else:
                        brackets += rgs[1][2][1]
                        t = type(rgs[0])
                        self._rg.append((rgs[1][:2] + t([brackets])))
                elif rgs[0][1] == rgs[1][1]:
                    idxs_to_remove.append(i)
                    idxs_to_remove.append(j)
                    brackets = ""
                    rgs_idx = None
                    if rgs[0][0] <= rgs[1][0]:
                        brackets += rgs[0][2][0]
                        rgs_idx = 0
                    else:
                        brackets += rgs[1][2][0]
                        rgs_idx = 1
                    if (rgs[1][2][1] == rgs[1][2][1] and rgs[0][2][1] == "]") or rgs[0][2][1] != rgs[1][2][1]:
                        brackets += "]"
                    else:
                        brackets += ")"
                    t = type(rgs[rgs_idx])
                    self._rg.append((rgs[rgs_idx][:2] + t([brackets])))
        idxs_to_remove.reverse()
        for idx in idxs_to_remove:
            self._rg.pop(idx)
        self._rg.sort(key=lambda x : x[0])
            
    def _get_intersection(self, old_rg, rg):
        ''' Used in intersect method '''
        new_rg = [None,None,""]
        if old_rg[0] > rg[0]:
            new_rg[0] = old_rg[0]
            new_rg[2] += old_rg[2][0]
        elif old_rg[0] == rg[0] and old_rg[2][0] != rg[2][0]:
            new_rg[0] = old_rg[0]
            new_rg[2] += "("
        else:
            new_rg[0] = rg[0]
            new_rg[2] += rg[2][0]
                    
        if old_rg[1] < rg[1]:
            new_rg[1] = old_rg[1]
            new_rg[2] += old_rg[2][1]
        elif old_rg[1] == rg[1] and old_rg[2][1] != rg[2][1]:
            new_rg[1] = old_rg[1]
            new_rg[2] += ")"
        else:
            new_rg[1] = rg[1]
            new_rg[2] += rg[2][1]
        return new_rg
    
    def value(self):
        out_str_arr = []
        for rg in self._rg:
            out_str_arr.append(rg[2][0] + str(rg[0]) + "," + str(rg[1]) + rg[2][1])
        return "\u222a".join(out_str_arr)
    
    def rand(self):
        ''' Returns a float within the object's range '''
        
        #First select a range index using a possibly overcomplicated algorithm
        #Set up this way so that the indexes have a weighted chance to be 
        # selected based on the size of the range
        seed = random()
        
        specific_range = []
        for rg in self._rg:
            specific_range.append(rg[1]-rg[0])
        total_range = sum(specific_range)
        
        chance = []
        running_total = 0
        for spec_rg in specific_range:
            x = spec_rg / total_range
            chance.append(running_total + x)
            running_total += x
        
        idx = None
        for i in range(len(chance)):
            if seed < chance[i]:
                idx = i
                break
        
        #Ban the numbers at the edges if they are not included in range
        banned = [None]
        if self._rg[idx][2][0] == '(': banned.append(self._rg[idx][0])
        if self._rg[idx][2][1] == ')': banned.append(self._rg[idx][1])
        num = None
        
        #Keep generating a random number to return until it is not a banned number
        while num in banned:
            num = random() * (self._rg[idx][1]-self._rg[idx][0]) + self._rg[idx][0]
        return num