# Open-World Fast Travel Map

A graph model of an open-world game map: locations are nodes, roads are
weighted edges (travel time), and the fast travel planner finds the quickest
route with Dijkstra's algorithm.

## Run
    python main.py
    python -m unittest -v

## Structure
    worldmap/graph.py         WorldMap class (adjacency list): add_location, add_route, neighbors
    worldmap/traversal.py     bfs, dfs
    worldmap/pathfinding.py   fastest_route (Dijkstra)
    worldmap/sample_world.py  the sample map
    main.py                   prints the results
    tests/test_worldmap.py    unit tests

## Graph design
- **Nodes:** TODO
- **Edges:** TODO
- **Directed or undirected:** TODO
- **Weights:** TODO
- **Why an adjacency list:** TODO

## Results
TODO: paste the output of main.py

## Test cases
| Test | What it tests | Expected | Actual |
|---|---|---|---|
| | | | |

## Reasoning
### Why this graph structure fits
TODO

### BFS vs DFS
TODO

### How Dijkstra works
TODO
