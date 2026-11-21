"""Fast travel route planner: Dijkstra's algorithm for the quickest route and total travel time between two locations."""

from heapq import heappop, heappush


def dijkstra(world, start):
    """Run Dijkstra's algorithm from start.

    Return (best_time, came_from):
        best_time: {location: fewest total hours from start}
        came_from: {location: the location just before it on the fastest route (start maps to None)}
    """
    # TODO 1: If start is not in the world, return ({}, {}).
    # TODO 2: Set best_time = {start: 0} and came_from = {start: None}.
    # TODO 3: Make the frontier, a heap of (total_time, location) tuples, starting with (0, start).
    # TODO 4: While the frontier is not empty:
    #     a. heappop the smallest (total_time, location).
    #     b. If total_time > best_time[location], it is an old, slower entry, so skip it (continue).
    #     c. Loop over world.neighbors(location).items() to get each (neighbor, hours).
    #        (.items() is needed because neighbors is a dict, unlike the list of tuples on the Ed slide.)
    #     d. candidate = total_time + hours
    #     e. If candidate < best_time.get(neighbor, float("inf")):
    #            set best_time[neighbor] = candidate
    #            set came_from[neighbor] = location
    #            heappush (candidate, neighbor) onto the frontier
    # TODO 5: Return best_time, came_from.
    raise NotImplementedError("TODO: write dijkstra")


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
