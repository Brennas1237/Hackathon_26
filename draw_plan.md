# The user draws a plan on the map, which is represented as a list of points. Each point has x and y coordinates, and may have additional attributes such as color or size.


The class has the abilities to define a shape
The shape starts as empty
The shape gets the following attributes:
- material
- temp

Then has the following attributes:
start draw
    define this as the origin
continue draw
    append all of the points
end draw
    if it is not touching any wall
        closes shape
    construct shape

close shape
    append all of the points to y = o to the list

construct shape
    essentially integrate
    for each x add in all of the y beneath
    these coordinates can get made into an efficient data structure by making points?
    return the data structure







