"""
Connection validator module for validating connections between AWS services.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from services.service_registry import ServiceRegistry


@dataclass
class ValidationResult:
    """Result of a connection validation."""
    is_valid: bool
    message: str
    required_services: Optional[List[str]] = None


class ConnectionValidator:
    """Validates connections between AWS services."""
    
    @classmethod
    def validate_connection(cls, source_id: str, target_id: str) -> ValidationResult:
        """
        Validate a connection between two services.
        
        Args:
            source_id: ID of the source service
            target_id: ID of the target service
            
        Returns:
            ValidationResult with validation status and message
        """
        # Get service information
        source_info = ServiceRegistry.get_service(source_id)
        target_info = ServiceRegistry.get_service(target_id)
        
        if not source_info or not target_info:
            return ValidationResult(
                is_valid=False,
                message="Invalid service ID"
            )
        
        # Check if target is in the allowed connections for source
        if target_id in source_info.connection_rules.get("direct", []):
            return ValidationResult(
                is_valid=True,
                message=f"Valid connection: {source_info.display_name} → {target_info.display_name}"
            )
        
        # Check if connection requires intermediate services
        for required_service in source_info.connection_rules.get("requires", []):
            required_target = required_service.get("target")
            if required_target == target_id:
                intermediates = required_service.get("intermediate", [])
                return ValidationResult(
                    is_valid=False,
                    message=f"{source_info.display_name} → {target_info.display_name} requires {', '.join(intermediates)}",
                    required_services=intermediates
                )
        
        # Connection is not allowed
        return ValidationResult(
            is_valid=False,
            message=f"{source_info.display_name} cannot connect directly to {target_info.display_name}"
        )