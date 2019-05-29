# FRange

A float-range class that handles unions and intersections. Created primarily to 
track the domains of functions.

Arguments for init, union, and intersect are in the form of iterables of iterables, like this:\n
rg = FRange(\[\[1,2,'(]'], \[3,4,'\[)']) , 
but can also input ranges in interval notation in a string, like this:\n 
rg.union(["(1,2]","[3,4)"]) .

Has a rand() method which returns a random number within the object's range.
