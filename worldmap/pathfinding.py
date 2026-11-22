"""Fast travel route planner: Dijkstra's algorithm for the quickest route and total travel time between two locations."""

from heapq import heappop, heappush


def dijkstra(world, start):
    """Run Dijkstra's algorithm from start.

    Return (best_time, came_from):
        best_time: {location: fewest total hours from start}
        came_from: {location: the location just before it on the fastest route (start maps to None)}
    """
    if start not in world:  # guard against non-existent locations
        return {}, {}
    best_time = {start: 0}
    came_from = {start: None}
    frontier = [(0, start)]  # heap of (total_time, location), smallest time on top

    while frontier:
        total_time, location = heappop(frontier)
        if total_time > best_time[location]:  # old, slower entry for a place already improved
            continue
        for neighbor, hours in world.get_neighbors(location).items():
            candidate = total_time + hours
            if candidate < best_time.get(neighbor, float("inf")):  # found a faster way there
                best_time[neighbor] = candidate
                came_from[neighbor] = location
                heappush(frontier, (candidate, neighbor))
    return best_time, came_from


def build_path(came_from, goal):
    """Follow came_from back from goal to the start and return the route in order, or None if goal was never reached."""
    if goal not in came_from:
        return None
    path = []
    step = goal
    while step is not None:
        path.append(step)
        step = came_from[step]
    return path[::-1]


def fastest_route(world, start, goal):
    """Return (route, hours) for the quickest trip from start to goal, or (None, None) if there is no route."""
    best_time, came_from = dijkstra(world, start)
    if goal not in best_time:
        return None, None
    return build_path(came_from, goal), best_time[goal]


def route_hours(world, route):
    """Add up the hours along a route (a list of locations). Return None if two stops are not connected."""
    total = 0
    for a, b in zip(route, route[1:]):
        hours = world.neighbors(a).get(b)
        if hours is None:
            return None
        total += hours
    return total
