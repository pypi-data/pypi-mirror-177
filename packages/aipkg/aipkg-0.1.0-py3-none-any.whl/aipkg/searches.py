from typing import Dict, Tuple, Union
from haversine import haversine
from queue import PriorityQueue
from typing import List

class Point:
    def __init__(self, name: str, x: int, y: int) -> None:
        self.name = name
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"{self.name}:[{self.x},{self.y}]"

class Graph:
    def __init__(self, nodes: int, names: List[Point]) -> None:
        self.nodes = nodes
        self.names = names
        self.g_dist = {}
        self.visited: Dict[str, int] = {}
        self.adj_list: Dict[str, List[Tuple[Point, float]]] = {}
        self.path = []
        self.parent = {}

        for point in self.names:
            self.adj_list[point.name] = []
            self.g_dist[point.name] = 0
            self.parent[point.name]: Dict[str, Union[str,int]] = -1
            self.visited[point.name] = 0

    def __find_distance(self, x1, x2, y1, y2) -> float:
        return haversine((x1, y1), (x2, y2))

    def reset(self):
        self.path = []
        for point in self.names:
            self.g_dist[point.name] = 0
            self.parent[point.name] = -1
            self.visited[point.name] = 0

    def addEdge(self, source: Point, destination: Point):
        distance = self.__find_distance(source.x, destination.x, source.y, destination.y)
        self.adj_list[source.name].append((destination, distance))
        self.adj_list[destination.name].append((source, distance))

    def printGraph(self):
        for point in self.names:
            all_adjancents = self.adj_list[point]
            for adjacent, distance in all_adjancents:
                print(f"{point} -> {adjacent.name} with distance {distance}")

    def dfs(self, source: Point, destination: Point):
        stack: List[Point] = [source]
        self.visited[source.name] = 1

        while stack:
            element = stack.pop()

            if element == destination:
                print("Goal has been found")
                break

            for neighbour, distance in self.adj_list[element.name]:
                if not self.visited[neighbour.name]:
                    stack.append(neighbour)
                    self.visited[neighbour.name] = 1
                    self.parent[neighbour.name] = element.name

    def bfs(self, source: Point, destination: Point):
        queue: List[Point] = [source]
        self.visited[source.name] = 1

        while queue:
            element = queue.pop(0)

            if element == destination:
                print("Goal has been found")
                break

            for neighbour, distance in self.adj_list[element.name]:
                if not self.visited[neighbour.name]:
                    queue.append(neighbour)
                    self.visited[neighbour.name] = 1
                    self.parent[neighbour.name] = element.name

    def gbfs(self, source: Point, destination: Point):
        pq: PriorityQueue = PriorityQueue()
        pq.put((0, source))
        self.visited[source.name] = 1

        while not pq.empty():
            element = pq.get()[1]

            if element == destination:
                print("Goal has been found")
                break

            for neighbour, distance in self.adj_list[element.name]:
                if not self.visited[neighbour.name]:
                    h_dist = self.__find_distance(neighbour.x, destination.x, neighbour.y, destination.y)
                    pq.put((h_dist, neighbour))
                    self.visited[neighbour.name] = 1
                    self.parent[neighbour.name] = element.name

    def a_star_search(self, source: Point, destination: Point):
        pq: PriorityQueue = PriorityQueue()
        pq.put((0, source))
        self.visited[source.name] = 1

        while not pq.empty():
            element = pq.get()[1]

            if element == destination:
                print("Goal has been reached")

            for neighbour, distance in self.adj_list[element.name]:
                if not self.visited[neighbour.name]:
                    h_dist = self.__find_distance(neighbour.x, destination.x, neighbour.y, destination.y)
                    self.g_dist[neighbour.name] = self.g_dist[element.name] + distance
                    f_dist = h_dist + self.g_dist[neighbour.name]

                    pq.put((f_dist, neighbour))
                    self.visited[neighbour.name] = 1
                    self.parent[neighbour.name] = element.name

    def print_path(self, j: str):
        if self.parent[j] == -1:
            print(j, end=" ")
            self.path.append(j)
            return
        self.print_path(self.parent[j])
        print(j, end=" ")
        self.path.append(j)