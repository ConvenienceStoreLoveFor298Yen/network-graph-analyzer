"""Loads the sample world map (a simplified Skyrim) from worldmap/data/skyrim.json.

Expected results to check against:
    Fastest route:     Solitude -> Riften = Solitude, Morthal, Whiterun, Riverwood,
                       Helgen, Ivarstead, Riften (17 hours)
    Fewest vs fastest: Whiterun -> Windhelm direct road is 8 hours (1 road), but
                       Whiterun -> Valtheim Towers -> Windhelm is faster (6 hours)
    One-way:           Throat of the World -> Riverwood = 1 hour,
                       Riverwood -> Throat of the World = 9 hours
    Unreachable:       Whiterun -> Raven Rock = no route
    Isolated:          Soul Cairn has no neighbors; BFS from it visits only itself
    Cycles:            Whiterun, Morthal, Dawnstar, Winterhold, Windhelm, Valtheim Towers
                       form a loop, so BFS/DFS must track visited locations
"""

import json

from worldmap.graph import WorldMap


def build_sample_world():
    with open("worldmap/data/skyrim.json") as f:
        data = json.load(f)
    world = WorldMap()
    for r in data["routes"]:
        world.add_route(r["from"], r["to"], r["hours"], one_way=r.get("one_way", False))
    for p in data["isolated"]:
        world.add_location(p["name"])
    return world
