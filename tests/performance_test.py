"""
Performance test module for evaluating architecture performance.
"""
from typing import Dict, List, Set, Tuple

from services.service_registry import ServiceRegistry


class PerformanceTest:
    """Evaluates the performance of AWS architectures."""
    
    @classmethod
    def estimate_latency(
        cls,
        services: List[str],
        connections: List[Tuple[str, str]]
    ) -> float:
        """
        Estimate the end-to-end latency of an architecture.
        
        Args:
            services: List of service IDs in the architecture
            connections: List of connections between services (source_id, target_id)
            
        Returns:
            Estimated latency in milliseconds
        """
        if not services:
            return 0.0
        
        # Calculate base service latencies
        service_latencies = {}
        for service_id in services:
            service_info = ServiceRegistry.get_service(service_id)
            if service_info:
                service_latencies[service_id] = service_info.latency_ms
        
        # Build a graph of the architecture
        graph = cls._build_graph(connections)
        
        # Find the critical path (path with highest latency)
        entry_points = cls._find_entry_points(graph)
        exit_points = cls._find_exit_points(graph)
        
        max_latency = 0.0
        for entry in entry_points:
            for exit in exit_points:
                path_latency = cls._calculate_path_latency(entry, exit, graph, service_latencies)
                max_latency = max(max_latency, path_latency)
        
        return max_latency
    
    @staticmethod
    def _build_graph(connections: List[Tuple[str, str]]) -> Dict[str, List[str]]:
        """
        Build a directed graph from connections.
        
        Args:
            connections: List of connections between services (source_id, target_id)
            
        Returns:
            Graph as an adjacency list
        """
        graph = {}
        
        for source, target in connections:
            if source not in graph:
                graph[source] = []
            if target not in graph:
                graph[target] = []
            
            graph[source].append(target)
        
        return graph
    
    @staticmethod
    def _find_entry_points(graph: Dict[str, List[str]]) -> List[str]:
        """
        Find entry points in the graph (nodes with no incoming edges).
        
        Args:
            graph: Graph as an adjacency list
            
        Returns:
            List of entry point service IDs
        """
        # Find all nodes that are targets
        targets = set()
        for source, target_list in graph.items():
            targets.update(target_list)
        
        # Entry points are nodes that are not targets
        entry_points = [node for node in graph if node not in targets]
        
        # If no entry points found, use any node as entry point
        if not entry_points and graph:
            entry_points = [next(iter(graph))]
        
        return entry_points
    
    @staticmethod
    def _find_exit_points(graph: Dict[str, List[str]]) -> List[str]:
        """
        Find exit points in the graph (nodes with no outgoing edges).
        
        Args:
            graph: Graph as an adjacency list
            
        Returns:
            List of exit point service IDs
        """
        exit_points = [node for node, targets in graph.items() if not targets]
        
        # If no exit points found, use any node as exit point
        if not exit_points and graph:
            exit_points = [next(iter(graph))]
        
        return exit_points
    
    @classmethod
    def _calculate_path_latency(
        cls,
        start: str,
        end: str,
        graph: Dict[str, List[str]],
        service_latencies: Dict[str, float]
    ) -> float:
        """
        Calculate the latency of a path from start to end.
        
        Args:
            start: Starting service ID
            end: Ending service ID
            graph: Graph as an adjacency list
            service_latencies: Dictionary of service latencies
            
        Returns:
            Path latency in milliseconds
        """
        # Use DFS to find all paths
        all_paths = []
        cls._find_all_paths(start, end, graph, [], all_paths)
        
        if not all_paths:
            return 0.0
        
        # Calculate latency for each path
        path_latencies = []
        for path in all_paths:
            latency = sum(service_latencies.get(service_id, 0.0) for service_id in path)
            path_latencies.append(latency)
        
        # Return the maximum latency
        return max(path_latencies) if path_latencies else 0.0
    
    @classmethod
    def _find_all_paths(
        cls,
        current: str,
        end: str,
        graph: Dict[str, List[str]],
        path: List[str],
        all_paths: List[List[str]]
    ) -> None:
        """
        Find all paths from current to end using DFS.
        
        Args:
            current: Current service ID
            end: Target service ID
            graph: Graph as an adjacency list
            path: Current path
            all_paths: List to store all found paths
        """
        # Add current node to path
        path.append(current)
        
        # If we reached the end, add the path to all_paths
        if current == end:
            all_paths.append(path.copy())
        else:
            # Explore all neighbors
            for neighbor in graph.get(current, []):
                # Avoid cycles
                if neighbor not in path:
                    cls._find_all_paths(neighbor, end, graph, path, all_paths)
        
        # Remove current node from path
        path.pop()