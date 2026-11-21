"""Demo program: prints the world map, BFS and DFS results, and example fastest routes."""

from worldmap.pathfinding import fastest_route, route_hours
from worldmap.sample_world import build_sample_world
from worldmap.traversal import bfs, dfs, fewest_roads, is_reachable


def check(label, func):
    """Run one check and print its result, or note that the code is still a TODO."""
    try:
        print(f"{label}: {func()}")
    except NotImplementedError as e:
        print(f"{label}: not done yet ({e})")


def main():
    world = build_sample_world()
    print(world)
    print()

    check("BFS from Whiterun", lambda: bfs(world, "Whiterun"))
    check("DFS from Whiterun", lambda: dfs(world, "Whiterun"))
    check("BFS from Soul Cairn (expect only Soul Cairn)", lambda: bfs(world, "Soul Cairn"))
    check("Whiterun can reach Raven Rock (expect False)", lambda: is_reachable(world, "Whiterun", "Raven Rock"))

    check("Fastest Solitude -> Riften (expect 17 hours)", lambda: fastest_route(world, "Solitude", "Riften"))
    check("Fewest roads Whiterun -> Windhelm", lambda: fewest_roads(world, "Whiterun", "Windhelm"))
    check("  ...those roads take (expect 8 hours)",
          lambda: route_hours(world, fewest_roads(world, "Whiterun", "Windhelm")))
    check("Fastest Whiterun -> Windhelm (expect 6 hours via Valtheim Towers)",
          lambda: fastest_route(world, "Whiterun", "Windhelm"))
    check("Fastest Throat of the World -> Riverwood (expect 1 hour)",
          lambda: fastest_route(world, "Throat of the World", "Riverwood"))
    check("Fastest Riverwood -> Throat of the World (expect 9 hours)",
          lambda: fastest_route(world, "Riverwood", "Throat of the World"))
    check("Fastest Whiterun -> Raven Rock (expect no route)",
          lambda: fastest_route(world, "Whiterun", "Raven Rock"))


if __name__ == "__main__":
    main()
