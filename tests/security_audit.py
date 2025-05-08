"""
Security audit module for evaluating architecture security.
"""
from typing import Dict, List, Optional, Set, Tuple


class SecurityAudit:
    """Performs security audits on AWS architectures."""
    
    @classmethod
    def audit_architecture(
        cls,
        services: List[str],
        connections: List[Tuple[str, str]],
        level_id: Optional[int] = None
    ) -> List[str]:
        """
        Audit an architecture for security issues.
        
        Args:
            services: List of service IDs in the architecture
            connections: List of connections between services (source_id, target_id)
            level_id: Optional level ID to apply level-specific rules
            
        Returns:
            List of security issues found
        """
        issues = []
        
        # Level 1-2 have simplified security requirements
        if level_id in [1, 2]:
            # For level 1 (Blog API), only check for IAM role with Lambda
            if level_id == 1:
                if "lambda" in services and "iam" not in services:
                    issues.append("Lambda function without IAM role")
            
            # For level 2 (Static Portfolio), check for CloudFront with S3
            elif level_id == 2:
                if "s3" in services and "cloudfront" not in services:
                    # Check if S3 is directly connected to API Gateway
                    for source, target in connections:
                        if source == "api_gateway" and target == "s3":
                            issues.append("S3 bucket is publicly accessible without CloudFront")
                            break
            
            return issues
        
        # For levels 3+, apply more comprehensive security checks
        
        # For levels 3+, only check for S3 encryption if KMS is in the required or optional services
        # This is a simplification since we don't have direct access to available_services here
        if level_id and level_id >= 3:
            if "s3" in services and "kms" in services and not any(conn[0] == "kms" and conn[1] == "s3" for conn in connections):
                issues.append("S3 bucket is not encrypted with KMS")
        
        # Check for public S3 buckets without CloudFront
        if "s3" in services and "cloudfront" not in services:
            # Check if S3 is directly connected to API Gateway or Internet Gateway
            for source, target in connections:
                if (source == "api_gateway" and target == "s3") or (source == "internet_gateway" and target == "s3"):
                    issues.append("S3 bucket is publicly accessible without CloudFront")
                    break
        
        # Check for Lambda functions without IAM roles
        if "lambda" in services and "iam" not in services:
            issues.append("Lambda function without IAM role")
        
        # Check for RDS without encryption (only if KMS is being used)
        if "rds" in services and "kms" in services and not any(conn[0] == "kms" and conn[1] == "rds" for conn in connections):
            issues.append("RDS database is not encrypted")
        
        # Check for RDS without VPC
        if "rds" in services and "vpc" not in services:
            issues.append("RDS database is not in a VPC")
        
        # Check for API Gateway without WAF (only if WAF is being used and level requires it)
        if "api_gateway" in services and "waf" in services and cls._requires_waf(services) and not any(conn[0] == "waf" and conn[1] == "api_gateway" for conn in connections):
            issues.append("API Gateway without WAF protection")
        
        # Check for missing authentication (only if authentication services are available)
        auth_services = {"cognito", "iam"}.intersection(set(services))
        if cls._requires_auth(services) and not auth_services and (level_id is None or level_id >= 3):
            issues.append("Architecture lacks authentication mechanism")
        
        return issues
    
    @staticmethod
    def _requires_waf(services: List[str]) -> bool:
        """
        Check if the architecture requires WAF based on services used.
        
        Args:
            services: List of service IDs in the architecture
            
        Returns:
            True if WAF is required, False otherwise
        """
        # WAF is required for architectures with API Gateway and at least one of these services
        high_risk_services = {"rds", "dynamodb", "lambda", "ec2"}
        return "api_gateway" in services and any(service in high_risk_services for service in services)
    
    @staticmethod
    def _requires_auth(services: List[str]) -> bool:
        """
        Check if the architecture requires authentication.
        
        Args:
            services: List of service IDs in the architecture
            
        Returns:
            True if authentication is required, False otherwise
        """
        # Authentication is required for architectures with these services
        auth_required_services = {"rds", "dynamodb", "lambda", "ec2", "s3"}
        return any(service in auth_required_services for service in services)