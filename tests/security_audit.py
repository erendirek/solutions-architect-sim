"""
Security audit module for evaluating architecture security.
"""
from typing import Dict, List, Set, Tuple


class SecurityAudit:
    """Performs security audits on AWS architectures."""
    
    @classmethod
    def audit_architecture(
        cls,
        services: List[str],
        connections: List[Tuple[str, str]]
    ) -> List[str]:
        """
        Audit an architecture for security issues.
        
        Args:
            services: List of service IDs in the architecture
            connections: List of connections between services (source_id, target_id)
            
        Returns:
            List of security issues found
        """
        issues = []
        
        # Check for unencrypted S3 buckets
        if "s3" in services and "kms" not in services:
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
        
        # Check for RDS without encryption
        if "rds" in services and "kms" not in services:
            issues.append("RDS database is not encrypted")
        
        # Check for RDS without VPC
        if "rds" in services and "vpc" not in services:
            issues.append("RDS database is not in a VPC")
        
        # Check for API Gateway without WAF for levels that require it
        if "api_gateway" in services and cls._requires_waf(services) and "waf" not in services:
            issues.append("API Gateway without WAF protection")
        
        # Check for missing authentication
        if cls._requires_auth(services) and "cognito" not in services and "iam" not in services:
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