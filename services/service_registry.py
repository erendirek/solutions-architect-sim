"""
Service registry module for managing AWS service definitions.
"""
import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class ServiceInfo:
    """Information about an AWS service."""
    service_id: str
    display_name: str
    description: str
    category: str
    icon_path: str
    cost_per_hour: float
    latency_ms: float
    connection_rules: Dict[str, List[str]]


class ServiceRegistry:
    """Registry for AWS services used in the game."""
    
    _services: Dict[str, ServiceInfo] = {}
    _initialized: bool = False
    
    @classmethod
    def initialize(cls) -> None:
        """Initialize the service registry by loading service definitions."""
        if cls._initialized:
            return
            
        # Load service definitions from JSON file
        services_file = os.path.join("config", "services.json")
        if os.path.exists(services_file):
            with open(services_file, "r") as f:
                services_data = json.load(f)
                
            for service_id, data in services_data.items():
                cls._services[service_id] = ServiceInfo(
                    service_id=service_id,
                    display_name=data["display_name"],
                    description=data["description"],
                    category=data["category"],
                    icon_path=data["icon_path"],
                    cost_per_hour=data["cost_per_hour"],
                    latency_ms=data["latency_ms"],
                    connection_rules=data["connection_rules"]
                )
        
        cls._initialized = True
    
    @classmethod
    def get_service(cls, service_id: str) -> Optional[ServiceInfo]:
        """
        Get service information by ID.
        
        Args:
            service_id: ID of the service to retrieve
            
        Returns:
            ServiceInfo object if found, None otherwise
        """
        if not cls._initialized:
            cls.initialize()
            
        return cls._services.get(service_id)
    
    @classmethod
    def get_all_services(cls) -> Dict[str, ServiceInfo]:
        """
        Get all registered services.
        
        Returns:
            Dictionary of service ID to ServiceInfo
        """
        if not cls._initialized:
            cls.initialize()
            
        return cls._services
    
    @classmethod
    def get_services_by_category(cls, category: str) -> Dict[str, ServiceInfo]:
        """
        Get services filtered by category.
        
        Args:
            category: Category to filter by
            
        Returns:
            Dictionary of service ID to ServiceInfo for services in the category
        """
        if not cls._initialized:
            cls.initialize()
            
        return {
            service_id: info
            for service_id, info in cls._services.items()
            if info.category == category
        }