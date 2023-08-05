# pathfinding

## Table of content
- [table of content](#Table-of-content)
- [Installation](#Installation)
- [Note](#Note)
    - [Known issues](#Known-issues-)
- [Use](#Use)
    - [Create an instance](#Create-an-instance)
    - [Steps to find a path](#Steps-to-find-a-path)
    - [Display the path](#Display-the-path)

## Installation
You can install the package by running the following command :
```python3 -m pip install --upgrade PathFinder``` 

## Note 
**Please note** that the package is currently in **beta** version and may encounter **bugs** or **unexpected behaviours** for which **I am not responsible**.

#### Known issues : 
- No cartesian coordinates for grid display available (only alphabetical coordinates)
- Grid display is not centered and might not work in every terminal
- The `find_path` method is not optimized and might take a long time to find a path

## Use 

### Create an instance 
Simply import the `pathfinding` object from the package into your script and start use it.

```py
from pathfinding import PathFinder as pf

 # From Asynconf 2022 - https://asynconf.fr/
map = """
O___O_OO__OO__VO_O_O
__O___O_OOO_OO_____O
OO___O___OOO_OOOOO_O
__OO__X__OO_O___O__O
_OO___OO______O___OO
""".split("\n")

pathfinder = pf(
                        map,         # map to use (list or str)
                "X",                 # start point (str)
                "V",                 # end point (str)
                walkable="_",        # walkable tiles (str)
                non_walkable="O",    # non walkable tiles (str)
                debug_mode=False     # display processing informations (bool)
)
```

### Steps to find a path
1. Make a graph from the map
```py
graph = pathfinder.make_graph()
```
2. Get the first path found
```py
path = pathfinder.find_path()
```
3. Optimize the path
```py
optimized_path = pathfinder.optimize_path(path)
```
4. use the path
```py
print(pathfinder.get_path(alphanumeric=True))
print(pathfinder.get_path(alphanumeric=False))

##################################################
['G4', 'H4', 'I4', 'I5', 'J5', 'K5', 'L5', 'M5', 'N5', 'N4', 'O4', 'P4', 'P5', 'Q5', 'R5', 'R4', 'S4', 'S3', 'S2', 'R2', 'Q2', 'P2', 'O2', 'O1']
[(6, 3), (7, 3), (8, 3), (8, 4), (9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (13, 3), (14, 3), (15, 3), (15, 4), (16, 4), (17, 4), (17, 3), (18, 3), (18, 2), (18, 1), (17, 1), (16, 1), (15, 1), (14, 1), (14, 0)]
```
### Display the path
```py
print(pathfinder.show_path(show_grid=True, animate=False))

##################################################
# displays the path on the map. If animate is True, the path will be displayed step by step and the screen will be cleared after each step
```

