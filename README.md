# Open-World Fast Travel Map

A graph model of an open-world game map: locations are nodes, roads are
weighted edges (travel time), and the fast travel planner finds the quickest
route with Dijkstra's algorithm.

## Run
Run these from the project folder (the one containing `main.py`):

    python main.py
    python -m unittest -v

`python main.py` prints the map, then runs each
expected result from `sample_world.py`. Anything still unwritten shows as
"not done yet".

## Structure
    worldmap/graph.py         WorldMap class (weighted adjacency list)
                                Ed-style: add_vertex, add_edge (directed, weight 1 by default),
                                          get_neighbors, get_vertices, display
                                Project:  add_location, add_route (two-way unless one_way),
                                          neighbors, locations
    worldmap/traversal.py     bfs, dfs (TODO), is_reachable, fewest_roads
    worldmap/pathfinding.py   dijkstra (TODO), build_path, fastest_route, route_hours
    worldmap/sample_world.py  loads the sample map from data/skyrim.json
    worldmap/data/skyrim.json the sample map data (routes, hours, one-way and isolated places)
    main.py                   prints the map and checks results against the expected values
    tests/test_worldmap.py    unit tests

## Status
- Done: graph, sample data, `is_reachable`, `fewest_roads`, `build_path`, `fastest_route`, `route_hours`
- TODO: `bfs` and `dfs` in `traversal.py`, `dijkstra` in `pathfinding.py` (step-by-step TODOs are in each function)
- Done: 19 unit tests in `tests/test_worldmap.py` (15 will pass once bfs, dfs, and dijkstra are written)

## Sample data
The sample world is a simplified map of *The Elder Scrolls V: Skyrim* (Bethesda).
Location names come from the game ([UESP wiki](https://en.uesp.net/wiki/Skyrim:Transport)).
Travel times are invented for this project; Skyrim has no fixed travel-time table.
Expected test results were worked out by hand from these values.

The map includes a few special cases on purpose:
- **One-way route:** Throat of the World to Riverwood takes 1 hour (sliding down), but going back up takes 9 hours.
- **Fewest roads is not fastest:** Whiterun to Windhelm is 1 road (8 hours), but going through Valtheim Towers is faster (6 hours).
- **Unreachable places:** Raven Rock and Skaal Village are cut off from the mainland.
- **Isolated place:** Soul Cairn has no roads at all.
- **Cycles:** Whiterun, Morthal, Dawnstar, Winterhold, Windhelm, and Valtheim Towers form a loop.

## Graph design
- **Nodes:** locations (cities, villages, landmarks)
- **Edges:** roads between locations
- **Directed or undirected:** stored as directed edges. Roads are added in both directions, so they act two-way, and a route can be marked `one_way` (like sliding down from the Throat of the World).
- **Weights:** travel time in hours (default 1 if no weight is given)
- **Why an adjacency list:** the map is sparse (each location connects to only a few others), so storing only the roads that exist uses much less space than an adjacency matrix. The layout is `{location: {neighbor: hours}}`, the same as the weighted adjacency list in the course.

## Results
TODO: paste the output of `python main.py` once bfs, dfs, and dijkstra are written

## Test cases
Run `python -m unittest -v`. Tests are in `tests/test_worldmap.py`.
Fill in the Actual column from the test run once bfs, dfs, and dijkstra are written.

| Test | Type | What it tests | Expected | Actual |
|---|---|---|---|---|
| `test_add_edge_is_directed_with_default_weight` | Normal | add_edge is one-way with weight 1 | A has {B: 1}, B has no edges | TODO |
| `test_add_route_is_two_way` | Normal | add_route connects both ways | A to B and B to A, 4 hours each | TODO |
| `test_bfs_visits_every_mainland_location` | Normal | BFS from Whiterun reaches the whole mainland | all 17 mainland locations, starting with Whiterun | TODO |
| `test_bfs_visits_neighbors_before_farther_places` | Normal | BFS goes level by level | Whiterun's 5 neighbors come right after Whiterun | TODO |
| `test_dfs_goes_deep_first` | Normal | DFS follows one path before backing up | 3rd location is a neighbor of the 2nd | TODO |
| `test_bfs_has_no_duplicates` / `test_dfs_has_no_duplicates` | Repeated visits | Whiterun loop is not visited twice | no location appears twice | TODO |
| `test_small_cycle` | Repeated visits | A to B to C to A does not loop forever | A, B, C each once | TODO |
| `test_isolated_location` | Edge case | Soul Cairn has no roads | BFS and DFS return only Soul Cairn | TODO |
| `test_disconnected_island` | Edge case | Solstheim is separate from the mainland | BFS from Raven Rock finds only Raven Rock and Skaal Village | TODO |
| `test_unreachable_destination` | Edge case | Whiterun to Raven Rock | not reachable, no route (None, None) | TODO |
| `test_location_not_in_map` | Edge case | a place that does not exist | empty list and no route | TODO |
| `test_route_to_itself` | Edge case | Whiterun to Whiterun | route is just Whiterun, 0 hours | TODO |
| `test_long_route` | Shortest path | Solitude to Riften | Solitude, Morthal, Whiterun, Riverwood, Helgen, Ivarstead, Riften, 17 hours | TODO |
| `test_fastest_is_not_fewest_roads` | Shortest path | Whiterun to Windhelm | fewest roads is the direct road (8 hours), fastest is through Valtheim Towers (6 hours) | TODO |
| `test_one_way_route` | Shortest path | the one-way slide | down: 1 hour, back up: 9 hours | TODO |

## Time complexity
V is the number of locations (vertices) and E is the number of roads (edges).

| Operation | Time | Why |
|---|---|---|
| add_vertex / add_location | O(1) | one dictionary insert |
| add_edge / add_route | O(1) | one or two dictionary inserts |
| neighbors / get_neighbors | O(1) | one dictionary lookup |
| BFS / DFS | O(V + E) | each location is visited once and each road is checked once |
| fewest_roads | O(V + E) | same as BFS |
| Dijkstra (fastest_route) | O((V + E) log V) | each road can push onto the heap, and each heap push or pop costs log V |
| Space for the graph | O(V + E) | the adjacency list stores each location and each road once |

## Reasoning
### Why this graph structure fits
A fast travel map is naturally a graph: each location is a node, and each road
between two locations is an edge. Roads take different amounts of time to travel,
so the edges are weighted with hours. Most roads can be traveled both ways, so
`add_route` adds the edge in both directions, but the graph is stored as directed
edges so a one-way route like sliding down from the Throat of the World can be
represented too. An adjacency list fits because the map is sparse: each location
only connects to a few others, so storing just the roads that exist uses much less
space than a matrix with a slot for every pair of locations. It also makes the most
common operation, "what can I reach from here?", a single dictionary lookup.

### BFS vs DFS
Both searches start at one location and visit every location reachable from it,
using a visited set so the Whiterun loop (Morthal, Dawnstar, Winterhold, Windhelm,
Valtheim Towers) doesn't send them in circles. The difference is the order. BFS uses
a queue, so it visits all of Whiterun's direct neighbors first, then the places two
roads away, and so on, spreading outward in rings. DFS uses a stack, so it picks one
road and keeps following it as far as it can go before backing up to try another
road. Because BFS explores by number of roads, it can find the route with the fewest
roads, but it ignores travel time: from Whiterun to Windhelm it picks the direct
8-hour road, even though going through Valtheim Towers takes only 6 hours. DFS
doesn't find shortest routes at all, but it is useful for questions like "is this
place reachable?" Neither search ever reaches Raven Rock or the Soul Cairn from the
mainland, since no roads lead there.

### How Dijkstra works
Dijkstra's algorithm finds the fastest route by always expanding the location with
the smallest total travel time found so far. It starts with the starting location at
0 hours and keeps a priority queue (heap) of locations ordered by their total time.
Each step, it takes the closest location off the heap and checks each road leaving
it: if going through this location gives a neighbor a shorter total time than any
route found before, it records the new time, remembers which location it came from,
and pushes the neighbor onto the heap. Because it always takes the closest location
first, once a location comes off the heap its time is final. When it finishes, the
route is rebuilt by following the "came from" links backward from the destination.
This is why it finds Whiterun, Valtheim Towers, Windhelm (6 hours) instead of the
direct road (8 hours), and why Solitude to Riften goes through Whiterun and Ivarstead
for 17 hours. If a destination is never reached, like Raven Rock from Whiterun, there
is no route. Dijkstra works here because no travel time is negative.
