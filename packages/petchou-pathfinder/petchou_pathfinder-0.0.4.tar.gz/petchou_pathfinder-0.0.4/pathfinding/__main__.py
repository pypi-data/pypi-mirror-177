import os
import platform
import time

from termcolor import colored
import colorama

colorama.init()

ALPHABET = "!_ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# PathFinder instance
class PathFinder:
    def __init__(self, grid: str | list[str], start: str, end: str, walkable: str, non_walkable: str, debug_mode=False):
        self._grid = [
            line for line in grid if line != ""
        ] \
            if isinstance(grid, list) \
            else  [
            line for line in grid.split("\n") if line != ""
        ]
        self._start = start
        self._end = end
        self._walkable = walkable
        self._non_walkable = non_walkable
        self._debug_mode = debug_mode
        self._path = []
        self._path_found = False

    # show debug info
    def _print(self, *text: str):
        if self._debug_mode:
            text = " ".join([str(t) for t in text])
            print(text)

    # optimize the path
    def optimize_path(self):
        optimized_path = self._path
        shortcuts = [0]
        while shortcuts:
            shortcuts = []
            for pos in self._path:
                potential_shortcuts = self._graph.get(pos)

                if potential_shortcuts is not None:
                    for d in potential_shortcuts:
                        if d in self._path and pos in self._path:
                            pos_index = self._path.index(pos)
                            d_index = self._path.index(d)

                            if d_index - pos_index > 1:
                                shortcuts.append([pos_index, d_index])
                                break

            self._print(f"shortcuts : {shortcuts}")

            if shortcuts != []:
                shortcuts = [shortcuts[0]]
                print(f"{self._path[shortcuts[0][0]]} => {self._path[shortcuts[0][1]]}")

                offset = 0
                for pos_index, d_index in shortcuts:
                    self._print(self._path[pos_index], self._path[d_index])
                    pos_index -= offset
                    d_index -= offset
                    optimized_path = optimized_path[:pos_index + 1] + optimized_path[d_index:]
                    offset += d_index - pos_index - 1
                self._print(str(self._path) + " => " + str(optimized_path))
                self._path = optimized_path

        # 0 1 2 3 4 5 6 7 8 9 10
        self._path = optimized_path

    # make a graph from the grid
    def make_graph(self):
        # Principe : créer un dictionnaire qui pour chaque case associe
        # une liste des possibilités de déplacement
        # les obstacles ne sont pas dedans (car on ne peut pas aller dessus)

        # ajouter un cadre autour de la grille pour ne pas en sortir
        self._grid.insert(0, "O" * len(self._grid[0]))
        self._grid.append("O" * len(self._grid[0]))
        for row in self._grid:
            row = "O" + row + "O"
        graph = {}
        grid_dict = {}
        for y, row in enumerate(self._grid):
            for x, value in enumerate(row):
                grid_dict[f"{ALPHABET[x + 2]}{y}"] = value

        for node in grid_dict.keys():
            if grid_dict.get(node) == self._start:
                self.depart = node
            elif grid_dict.get(node) == self._end:
                self.arrive = node
            x, y = node[0], int(node[1:])
            top = f"{x}{y + 1}"
            bottom = f"{x}{y - 1}"
            right = f"{ALPHABET[ALPHABET.index(x) + 1]}{y}"
            left = f"{ALPHABET[ALPHABET.index(x) - 1]}{y}"

            if grid_dict.get(node) != "O":
                graph[node] = []

                if grid_dict.get(top) is not (None or "O") and ("0"
                                                                or "_" not in top):
                    graph[node].append(top)

                if grid_dict.get(bottom) is not (None or "O") and ("0" or "_"
                                                                   not in bottom):
                    graph[node].append(bottom)

                if grid_dict.get(left) is not (None or "O") and not ("0" in left):
                    if "_" not in left:
                        graph[node].append(left)

                if grid_dict.get(right) is not (None or "O") and ("0" or "_"
                                                                  not in right):
                    graph[node].append(right)

        self._print(graph)
        self._graph = graph
        return graph

    # print grid in a readable way
    def _show_grid(self, grid: list[list[str]]):
        grid = ["".join(line) for line in grid]
        grid = "\n".join(grid)
        return grid

    # show the path on the grid
    def show_path(self, show_grid=True, animate=False):
        try:
            path = self._path
        except AttributeError:
            print("Path not found, please find a path first.")
            return None
        grid = [list(line) for line in self._grid]

        end_node = colored("⬛", "blue")
        start_node = colored("⬛", "green")
        path_node = colored("⬛", "cyan")
        walkable_node = colored("⬛", "grey")
        non_walkable_node = colored("⬛", "red")

        # change nodes to colored ones
        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                if value == self._start:
                    grid[y][x] = start_node
                elif value == self._end:
                    grid[y][x] = end_node
                elif value == self._walkable:
                    grid[y][x] = walkable_node
                elif value == self._non_walkable:
                    grid[y][x] = non_walkable_node

        # delete first and last line
        grid.pop(0)
        grid.pop(-1)

        if show_grid:
            # add letters on top and numbers on the left
            for y, row in enumerate(grid):
                row.insert(0, str(y))
                grid[y] = row
            grid.insert(0, list("  " + " ".join(ALPHABET[2:len(grid[0]) +1])))

        if animate:
            # get current OS
            os_name = platform.system()
            path = [self._get_cartesian_coord(node) for node in path[1:-1]]
            time.sleep(0.2)

            os.system("cls" if os_name == "Windows" else "clear")
            for node in path:
                print(self._show_grid(grid))
                grid[node[1] + 1][node[0] + 1] = path_node
                time.sleep(0.2)
                os.system("cls" if os_name == "Windows" else "clear")

        else:
            path = [self._get_cartesian_coord(node) for node in path[1:-1]]
            for node in path:
                grid[node[1] + 1][node[0] + 1] = path_node

        return self._show_grid(grid)

    # find the shortest path
    def find_path(self, graph: dict = None):
        if graph is None:
            try:
                graph = self._graph
            except AttributeError:
                print("Graph not found, please make a graph first.")
                return None
        # init
        self._print("Init...")
        self._print(f"Depart: {self.depart}")
        self._print(f"End: {self.arrive}")
        self._print(f"Graph: {graph}")

        banned = []
        path = [self.depart]
        current = self.depart
        # pour chaque direction, vérifie qu'il ne revient pas sur ses pas
        # ou ne sera pas bloqué après
        # si c'est le cas, marque la case comme une impasse et revient sur ses pas
        # INFO : Ordre de recherche: haut, bas, gauche, droite
        while current != self.arrive:
            # check if the path exist
            possible = False
            for test in self._graph.get(self.depart):
                if [self.depart, test] in banned:
                    pass
                else:
                    possible = True

            if possible is False:
                self._print("Unable to find a path to the end point...")
                return None

            # directions possibles
            dirs = [d for d in graph.get(path[-1]) if path + [d] not in banned]
            self._print(path, "=>", dirs)
            done = False
            for d in dirs:
                if done is True:
                    pass
                else:
                    self._print("++++++++++++++++++")
                    self._print(path, "=>", d, "?")
                    next = graph.get(d)
                    next = [] if next is None else next
                    can_go = False  # permettra de gérer les non-existences
                    if not d in path:
                        for n in next:
                            new_path = path + [d, n]
                            if new_path not in banned and n not in path:
                                can_go = True
                        self._print("==> ", can_go)
                        if can_go is True or d == self.arrive:
                            path += [d]
                            self._print("Updated : ", path)
                            current = path[-1]
                            done = True
                        else:
                            banned.append(path + [d])
                            self._print("banned ", path + [d])
                            del path[-1]
                            self._print("new path : ", path)
                            self._print("banned: ", banned)
                            done = True

                        path = [self.depart] if path == [] else path
                    else:
                        self._print("==> False")
                    self._print("++++++++++++++++++")

        self._path = path
        self._path_found = True
        self._print(f"Path found: {path}")
        return path

    # get the path in cartesian coordonates or in alphanumeric type
    def get_path(self, alphanumeric=True):
        try:
            path = self._path
        except AttributeError:
            print("Path not found, please find a path first.")
            return None
        if alphanumeric:
            return path
        else:
            path = [self._get_cartesian_coord(p) for p in path]
            return path

    def _get_cartesian_coord(self, p):
        x = ALPHABET.index(p[0]) - 2
        y = int(p[1:]) - 1
        return x, y
