# FRange

A float-range class that handles unions and intersections. Created primarily to 
track the domains of functions.

 ### Argument Form  
Arguments for init, union, and intersect are in the form of iterables of iterables, which is how ranges are stored internally, and look like this:  
```>>> rg = FRange([ [1,2,'(]'], [3,4,'[)'] ]) ```  
but can also input ranges in interval notation in a string, like this:   
```>>> rg.union(["(1,2]", "[3,4)"]) ```  
The brackets work the way they do in interval notation, () not including the edge values, and [] including the edge values.  

 ### Methods  
The __value()__ method returns the range in a string, with discontinuous ranges being combined with a union character:  
``` "(1,2]∪[3,4)" ```  
The __union()__ and __intersect()__ methods work like the mathematical union and intersect operators. Union (∪) combines two separate intervals, and intersect (∩) yields the interval at the intersection of two intervals:  
```>>> rg1, rg2 = [FRange("(2,3)")] * 2 ```  
```>>> rg1.union("(4,5]") ```  
```>>> rg2.intersect("[2.4,4)") ```  
```>>> rg1.value() ```  
``` "(2,3)∪(4,5]" ```  
```>>> rg2.value() ```  
 ``` "[2.4,3)" ```  
The class also has a __rand()__ method which returns a random number within the object's range, and will eventually have a generator, as well.
