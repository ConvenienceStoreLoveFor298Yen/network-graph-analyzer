"""WorldMap graph: weighted adjacency list {vertex: {neighbor: weight}}, routes are two-way unless one_way, weights are travel hours (default 1)."""


class WorldMap:
    def __init__(self):
        self.adj = {}

    def add_vertex(self, vertex):
        """Add a vertex; does nothing if it already exists."""
        if vertex not in self.adj:
            self.adj[vertex] = {}

    def add_edge(self, from_vertex, to_vertex, weight=1):
        """Add a directed edge from_vertex -> to_vertex with a weight (default 1).

        Missing vertices are added automatically.
        """
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        self.adj[from_vertex][to_vertex] = weight

    def get_neighbors(self, vertex):
        """Return {neighbor: weight} for a vertex (empty if it has no edges or doesn't exist)."""
        return self.adj.get(vertex, {})

    def get_vertices(self):
        """Return a list of every vertex."""
        return list(self.adj)

    def display(self):
        """Print the current structure of the graph."""
        print(self)

    def add_location(self, name):
        """Add a location (same as add_vertex)."""
        self.add_vertex(name)

    def add_route(self, a, b, hours, one_way=False):
        """Add a road between two locations.

        Roads go both ways, so this adds two directed edges (a -> b and b -> a),
        unless one_way is True.
        """
        self.add_edge(a, b, hours)
        if not one_way:
            self.add_edge(b, a, hours)

    def neighbors(self, name):
        """Return {neighbor: hours} for a location (same as get_neighbors)."""
        return self.get_neighbors(name)

    def locations(self):
        """Return a list of every location (same as get_vertices)."""
        return self.get_vertices()

    def __contains__(self, name):
        return name in self.adj

    def __str__(self):
        lines = []
        for name, routes in self.adj.items():
            links = ", ".join(f"{n} ({w})" for n, w in routes.items()) or "(no edges)"
            lines.append(f"{name} -> {links}")
        return "\n".join(lines)
