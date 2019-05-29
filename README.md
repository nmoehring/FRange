# FRange

A float-range class that handles unions and intersections. Created primarily to 
track the domains of functions.

 __Argument Form__  
Arguments for init, union, and intersect are in the form of iterables of iterables, which is how ranges are stored internally, and look like this:  
``` rg = FRange([ [1,2,'(]'], [3,4,'[)'] ]) ```  
but can also input ranges in interval notation in a string, like this:   
``` rg.union(["(1,2]", "[3,4)"]) ```

 __Other Features__  
The class also has a rand() method which returns a random number within the object's range, and will eventually have a generator, as well.
