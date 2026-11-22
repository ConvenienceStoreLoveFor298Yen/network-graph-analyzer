"""Breadth-first search and depth-first search over the world map, returning locations in visit order."""

from collections import deque


def bfs(world, start):
    """Breadth-first search from start. Return a list of locations in the order they are visited."""
    if start not in world: # guard against non-existent locations
        return []
    visited = {start}
    order = []
    queue = deque([start])

    while queue:
        location = queue.popleft()
        order.append(location)
        for neighbor_name in world.get_neighbors(location):
            if neighbor_name not in visited:
                visited.add(neighbor_name)  # mark when queued so nothing is queued twice
                queue.append(neighbor_name)
    return order


def dfs(world, start):
    """Depth-first search from start. Return a list of locations in the order they are visited."""
    if start not in world:  # guard against non-existent locations
        return []
    visited = set()  # empty: start is marked visited when it is popped
    order = []
    stack = [start]

    while stack:
        location = stack.pop()
        if location in visited:  # same place pushed twice by two different roads
            continue
        visited.add(location)
        order.append(location)
        # push in reverse so the first neighbor ends up on top and is visited first
        for neighbor_name in reversed(world.get_neighbors(location)):
            if neighbor_name not in visited:
                stack.append(neighbor_name)
    return order


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
