"""Breadth-first search and depth-first search over the world map, returning locations in visit order."""

from collections import deque

from worldmap.pathfinding import build_path


def _bfs_search(world, start):
    """Run BFS from start. Return (order, came_from).

    order:     locations in the order they are visited
    came_from: {location: the location it was first reached from (start maps to None)}.
               Its keys also act as the visited set.
    """
    if start not in world:  # guard against non-existent locations
        return [], {}
    came_from = {start: None}
    order = []
    queue = deque([start])

    while queue:
        location = queue.popleft()
        order.append(location)
        for neighbor_name in world.get_neighbors(location):
            if neighbor_name not in came_from:  # mark when queued so nothing is queued twice
                came_from[neighbor_name] = location
                queue.append(neighbor_name)
    return order, came_from


def bfs(world, start):
    """Breadth-first search from start. Return a list of locations in the order they are visited."""
    order, _ = _bfs_search(world, start)
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
    _, came_from = _bfs_search(world, start)
    return goal in came_from


def fewest_roads(world, start, goal):
    """Return the route from start to goal that uses the fewest roads (ignores hours), or None if unreachable.

    BFS reaches each location by the fewest roads first, so following came_from back from goal gives that route.
    """
    _, came_from = _bfs_search(world, start)
    return build_path(came_from, goal)
