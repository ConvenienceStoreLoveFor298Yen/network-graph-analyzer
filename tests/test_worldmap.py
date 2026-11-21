"""Unit tests for the world map graph, BFS/DFS traversal, and fastest route, including edge cases."""

import unittest

from worldmap.graph import WorldMap
from worldmap.pathfinding import fastest_route, route_hours
from worldmap.sample_world import build_sample_world
from worldmap.traversal import bfs, dfs, fewest_roads, is_reachable

MAINLAND = {
    "Whiterun", "Riverwood", "Helgen", "Falkreath", "Ivarstead", "Riften",
    "High Hrothgar", "Throat of the World", "Rorikstead", "Markarth", "Morthal",
    "Solitude", "Dragon Bridge", "Windhelm", "Valtheim Towers", "Winterhold", "Dawnstar",
}


class TestGraphStructure(unittest.TestCase):
    """Normal case: building the graph."""

    def test_add_vertex_no_duplicates(self):
        world = WorldMap()
        world.add_vertex("A")
        world.add_vertex("A")
        self.assertEqual(world.get_vertices(), ["A"])

    def test_add_edge_is_directed_with_default_weight(self):
        world = WorldMap()
        world.add_edge("A", "B")
        self.assertEqual(world.get_neighbors("A"), {"B": 1})
        self.assertEqual(world.get_neighbors("B"), {})

    def test_add_route_is_two_way(self):
        world = WorldMap()
        world.add_route("A", "B", 4)
        self.assertEqual(world.neighbors("A"), {"B": 4})
        self.assertEqual(world.neighbors("B"), {"A": 4})

    def test_sample_world_connections(self):
        world = build_sample_world()
        self.assertEqual(len(world.locations()), 20)
        self.assertEqual(world.neighbors("Riverwood"), {"Helgen": 2, "Whiterun": 2, "Falkreath": 3})


class TestTraversals(unittest.TestCase):
    """Normal case: BFS and DFS on the sample world."""

    def setUp(self):
        self.world = build_sample_world()

    def test_bfs_visits_every_mainland_location(self):
        order = bfs(self.world, "Whiterun")
        self.assertEqual(order[0], "Whiterun")
        self.assertEqual(set(order), MAINLAND)

    def test_bfs_visits_neighbors_before_farther_places(self):
        order = bfs(self.world, "Whiterun")
        first_ring = set(self.world.neighbors("Whiterun"))
        self.assertEqual(set(order[1:1 + len(first_ring)]), first_ring)

    def test_dfs_visits_every_mainland_location(self):
        order = dfs(self.world, "Whiterun")
        self.assertEqual(order[0], "Whiterun")
        self.assertEqual(set(order), MAINLAND)

    def test_dfs_goes_deep_first(self):
        order = dfs(self.world, "Whiterun")
        self.assertIn(order[2], self.world.neighbors(order[1]))


class TestRepeatedVisits(unittest.TestCase):
    """Repeated visits: the Whiterun loop must not cause duplicates or an endless loop."""

    def setUp(self):
        self.world = build_sample_world()

    def test_bfs_has_no_duplicates(self):
        order = bfs(self.world, "Whiterun")
        self.assertEqual(len(order), len(set(order)))

    def test_dfs_has_no_duplicates(self):
        order = dfs(self.world, "Whiterun")
        self.assertEqual(len(order), len(set(order)))

    def test_small_cycle(self):
        world = WorldMap()
        world.add_route("A", "B", 1)
        world.add_route("B", "C", 1)
        world.add_route("C", "A", 1)
        self.assertEqual(sorted(bfs(world, "A")), ["A", "B", "C"])
        self.assertEqual(sorted(dfs(world, "A")), ["A", "B", "C"])


class TestEdgeCases(unittest.TestCase):
    """Edge cases: no neighbors, disconnected parts, unreachable or missing locations."""

    def setUp(self):
        self.world = build_sample_world()

    def test_isolated_location(self):
        self.assertEqual(self.world.neighbors("Soul Cairn"), {})
        self.assertEqual(bfs(self.world, "Soul Cairn"), ["Soul Cairn"])
        self.assertEqual(dfs(self.world, "Soul Cairn"), ["Soul Cairn"])

    def test_disconnected_island(self):
        self.assertEqual(set(bfs(self.world, "Raven Rock")), {"Raven Rock", "Skaal Village"})

    def test_unreachable_destination(self):
        self.assertFalse(is_reachable(self.world, "Whiterun", "Raven Rock"))
        self.assertEqual(fastest_route(self.world, "Whiterun", "Raven Rock"), (None, None))
        self.assertIsNone(fewest_roads(self.world, "Whiterun", "Raven Rock"))

    def test_location_not_in_map(self):
        self.assertEqual(bfs(self.world, "Sovngarde"), [])
        self.assertEqual(dfs(self.world, "Sovngarde"), [])
        self.assertEqual(fastest_route(self.world, "Sovngarde", "Whiterun"), (None, None))

    def test_route_to_itself(self):
        self.assertEqual(fastest_route(self.world, "Whiterun", "Whiterun"), (["Whiterun"], 0))


class TestShortestPath(unittest.TestCase):
    """Shortest path: Dijkstra results that can be checked by hand on the sample world."""

    def setUp(self):
        self.world = build_sample_world()

    def test_long_route(self):
        route, hours = fastest_route(self.world, "Solitude", "Riften")
        self.assertEqual(route, ["Solitude", "Morthal", "Whiterun", "Riverwood", "Helgen", "Ivarstead", "Riften"])
        self.assertEqual(hours, 17)
        self.assertEqual(route_hours(self.world, route), 17)

    def test_fastest_is_not_fewest_roads(self):
        self.assertEqual(fewest_roads(self.world, "Whiterun", "Windhelm"), ["Whiterun", "Windhelm"])
        route, hours = fastest_route(self.world, "Whiterun", "Windhelm")
        self.assertEqual(route, ["Whiterun", "Valtheim Towers", "Windhelm"])
        self.assertEqual(hours, 6)

    def test_one_way_route(self):
        self.assertEqual(fastest_route(self.world, "Throat of the World", "Riverwood")[1], 1)
        self.assertEqual(fastest_route(self.world, "Riverwood", "Throat of the World")[1], 9)


if __name__ == "__main__":
    unittest.main()
