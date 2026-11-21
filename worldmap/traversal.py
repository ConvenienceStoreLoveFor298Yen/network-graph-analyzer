"""Breadth-first search and depth-first search over the world map, returning locations in visit order."""

from collections import deque


def bfs(world, start):
    """Breadth-first search from start. Return a list of locations in the order they are visited."""
    if start not in world: #guard against unreachable locations
        return []
    visited = set()
    order = []
    queue = deque()
   
    while queue:
       location = queue.popleft()
       order.append(location)
       for neighbor_name in world.get_neighbors(location):
           if neighbor_name not in visited:
               visited.add(neighbor_name)
               queue.append(neighbor_name)
    return order


def dfs(world, start):
    """Depth-first search from start. Return a list of locations in the order they are visited."""
    # TODO 1: If start is not in the world, return an empty list.
    # TODO 2: Make a set called visited (empty), a list called order (empty), and a stack (list) holding start.
    # TODO 3: While the stack is not empty:
    #     a. Pop a location from the END of the stack.
    #     b. If it is already in visited, skip it (continue).
    #     c. Add it to visited and append it to order.
    #     d. Push each neighbor in world.neighbors(location) that is not in visited onto the stack.
    #        Tip: push them in reversed order if you want neighbors visited in the order they were added.
    # TODO 4: Return order.
    # (Recursive version is fine too: a helper that visits a location, then calls itself on each unvisited neighbor.)
    raise NotImplementedError("TODO: write dfs")


def is_reachable(world, start, goal):
    """Return True if goal can be reached from start by following routes."""
    if start not in world or goal not in world:
        return False
    return goal in bfs(world, start)


def fewest_roads(world, start, goal):
    """Return the route from start to goal that uses the fewest roads (ignores hours), or None if unreachable.

    Uses the same idea as BFS, but remembers where each location was reached from.
    """
    if start not in world or goal not in world:
        return None
    came_from = {start: None}
    queue = deque([start])
    while queue:
        location = queue.popleft()
        if location == goal:
            break
        for neighbor in world.neighbors(location):
            if neighbor not in came_from:
                came_from[neighbor] = location
                queue.append(neighbor)
    if goal not in came_from:
        return None
    path = []
    step = goal
    while step is not None:
        path.append(step)
        step = came_from[step]
    return path[::-1]
