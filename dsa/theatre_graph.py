"""
Graph Representation & Dijkstra's Algorithm for Delhi NCR Theatres
Module: dsa.theatre_graph
Academic Concept: Weighted Undirected Graph, Adjacency List, Dijkstra's Shortest Path Algorithm

Time Complexity:
- Dijkstra's Algorithm: O((V + E) log V) using binary min-heap
- BFS Traversal: O(V + E)
Space Complexity: O(V + E)
"""

import heapq
from typing import Dict, List, Tuple, Optional, Any


class TheatreGraph:
    """
    Weighted Graph modeling the road network connecting CineSeat cinema multiplexes
    and major urban hubs across Delhi NCR.
    
    Venues:
    - CineSeat Citylight: Connaught Place (Central Delhi)
    - CineSeat Aurora: Saket (South Delhi)
    - CineSeat Horizon: Noida Sector 18 (Noida / East NCR)
    - Connecting Hubs: Cyber City (Gurgaon), Nehru Place, Karol Bagh
    """

    def __init__(self):
        # Adjacency list: node -> List of (neighbor, distance_in_km)
        self.adj: Dict[str, List[Tuple[str, float]]] = {}
        self.venues = {
            "citylight": {"name": "CineSeat Citylight", "hub": "Connaught Place", "area": "Central Delhi"},
            "aurora": {"name": "CineSeat Aurora", "hub": "Saket", "area": "South Delhi"},
            "horizon": {"name": "CineSeat Horizon", "hub": "Noida Sector 18", "area": "Noida"}
        }
        self._build_default_ncr_network()

    def add_edge(self, u: str, v: str, weight: float) -> None:
        """Add bidirectional road link between two locations in O(1) time."""
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight))

    def _build_default_ncr_network(self) -> None:
        """Populate realistic road distances (in km) across Delhi NCR."""
        roads = [
            ("Connaught Place", "Karol Bagh", 4.2),
            ("Connaught Place", "Nehru Place", 13.5),
            ("Connaught Place", "Noida Sector 18", 16.8),
            ("Karol Bagh", "Cyber City", 26.4),
            ("Nehru Place", "Saket", 5.6),
            ("Nehru Place", "Noida Sector 18", 9.2),
            ("Saket", "Cyber City", 17.5),
            ("Saket", "Noida Sector 18", 18.0),
            ("Cyber City", "Noida Sector 18", 34.0),
        ]
        for u, v, w in roads:
            self.add_edge(u, v, w)

    def dijkstra_shortest_path(self, start: str, destination: str) -> Tuple[float, List[str]]:
        """
        Dijkstra's Shortest Path Algorithm.
        Finds the minimal distance and path between start location and target destination.
        
        Time Complexity: O((V + E) log V)
        Space Complexity: O(V)
        """
        if start not in self.adj or destination not in self.adj:
            return float('inf'), []

        # Min-heap stores tuples of (distance, current_node)
        pq: List[Tuple[float, str]] = [(0.0, start)]
        distances: Dict[str, float] = {node: float('inf') for node in self.adj}
        distances[start] = 0.0
        previous_nodes: Dict[str, Optional[str]] = {node: None for node in self.adj}

        while pq:
            current_dist, current_node = heapq.heappop(pq)

            if current_node == destination:
                break

            if current_dist > distances[current_node]:
                continue

            for neighbor, weight in self.adj.get(current_node, []):
                distance_through_curr = current_dist + weight
                if distance_through_curr < distances[neighbor]:
                    distances[neighbor] = distance_through_curr
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance_through_curr, neighbor))

        # Reconstruct path
        path: List[str] = []
        curr: Optional[str] = destination
        while curr:
            path.append(curr)
            curr = previous_nodes.get(curr)
        path.reverse()

        if distances[destination] == float('inf'):
            return float('inf'), []
        return round(distances[destination], 1), path

    def find_nearest_theatre(self, user_hub: str) -> Dict[str, Any]:
        """
        Evaluate shortest routes from user location to all CineSeat theatres
        and return the nearest venue with route details.
        """
        if user_hub not in self.adj:
            user_hub = "Connaught Place"

        results = []
        for venue_id, info in self.venues.items():
            theatre_hub = info["hub"]
            dist, path = self.dijkstra_shortest_path(user_hub, theatre_hub)
            est_minutes = int(dist * 2.5)  # Est travel time at average 25 km/h traffic
            results.append({
                "theatreId": venue_id,
                "theatreName": info["name"],
                "hub": theatre_hub,
                "area": info["area"],
                "distanceKm": dist,
                "travelMinutes": est_minutes,
                "route": path
            })

        results.sort(key=lambda x: x["distanceKm"])
        return {
            "userLocation": user_hub,
            "nearest": results[0],
            "allVenues": results
        }

    def get_network_graph(self) -> Dict[str, Any]:
        """Export graph nodes and edges for visualization in the UI."""
        nodes = [{"id": k, "label": k} for k in self.adj.keys()]
        edges = []
        seen = set()
        for u in self.adj:
            for v, w in self.adj[u]:
                edge_id = tuple(sorted([u, v]))
                if edge_id not in seen:
                    seen.add(edge_id)
                    edges.append({"from": u, "to": v, "distance": w})
        return {"nodes": nodes, "edges": edges}
