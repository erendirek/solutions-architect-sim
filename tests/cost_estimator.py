"""
Cost estimator module for calculating architecture costs.
"""
from typing import Dict, List, Tuple

from services.service_registry import ServiceRegistry


class CostEstimator:
    """Estimates the cost of AWS architectures."""
    
    # Hours in a month (30 days)
    HOURS_PER_MONTH = 30 * 24
    
    @classmethod
    def estimate_monthly_cost(
        cls,
        services: List[str],
        connections: List[Tuple[str, str]]
    ) -> float:
        """
        Estimate the monthly cost of an architecture.
        
        Args:
            services: List of service IDs in the architecture
            connections: List of connections between services (source_id, target_id)
            
        Returns:
            Estimated monthly cost in USD
        """
        total_cost = 0.0
        
        # Calculate base service costs
        for service_id in services:
            service_info = ServiceRegistry.get_service(service_id)
            if service_info:
                # Calculate monthly cost based on hourly rate
                service_cost = service_info.cost_per_hour * cls.HOURS_PER_MONTH
                
                # Apply service-specific adjustments
                service_cost = cls._adjust_service_cost(service_id, service_cost, services, connections)
                
                total_cost += service_cost
        
        # Calculate data transfer costs
        data_transfer_cost = cls._calculate_data_transfer_cost(services, connections)
        total_cost += data_transfer_cost
        
        return total_cost
    
    @classmethod
    def _adjust_service_cost(
        cls,
        service_id: str,
        base_cost: float,
        services: List[str],
        connections: List[Tuple[str, str]]
    ) -> float:
        """
        Apply service-specific cost adjustments.
        
        Args:
            service_id: ID of the service
            base_cost: Base monthly cost
            services: List of all services in the architecture
            connections: List of connections between services
            
        Returns:
            Adjusted cost
        """
        adjusted_cost = base_cost
        
        # Apply service-specific adjustments
        if service_id == "lambda":
            # Lambda costs less if it's not frequently invoked
            if not any(source == "api_gateway" for source, target in connections if target == "lambda"):
                adjusted_cost *= 0.5
        
        elif service_id == "s3":
            # S3 costs less with lifecycle policies
            if "s3_lifecycle" in services:
                adjusted_cost *= 0.7
        
        elif service_id == "dynamodb":
            # DynamoDB costs less with auto scaling
            if "dynamodb_autoscaling" in services:
                adjusted_cost *= 0.8
        
        elif service_id == "ec2":
            # EC2 costs less with auto scaling
            if "auto_scaling" in services:
                adjusted_cost *= 0.8
            
            # EC2 costs less with reserved instances
            if "reserved_instances" in services:
                adjusted_cost *= 0.6
        
        return adjusted_cost
    
    @classmethod
    def _calculate_data_transfer_cost(
        cls,
        services: List[str],
        connections: List[Tuple[str, str]]
    ) -> float:
        """
        Calculate data transfer costs.
        
        Args:
            services: List of service IDs in the architecture
            connections: List of connections between services
            
        Returns:
            Data transfer cost
        """
        # Simplified data transfer cost calculation
        # In a real implementation, this would be more complex based on actual data transfer patterns
        
        # Base data transfer cost per connection
        cost_per_connection = 5.0
        
        # Count connections that incur data transfer costs
        billable_connections = 0
        for source, target in connections:
            # Skip connections if either service doesn't exist anymore
            if source not in services or target not in services:
                continue
                
            # Skip connections that don't incur data transfer costs
            if source == "cloudfront" and target == "s3":
                continue
            if source == "lambda" and target == "dynamodb":
                continue
            
            # Count billable connections
            billable_connections += 1
        
        return billable_connections * cost_per_connection