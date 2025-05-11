"""
Architecture validator module for evaluating architecture designs.
"""
from typing import Dict, List, Optional, Set, Tuple

from services.service_registry import ServiceRegistry


class ArchitectureValidator:
    """Validates AWS architectures against level requirements."""
    
    @classmethod
    def validate_architecture(
        cls,
        level_id: int,
        services: List[str],
        connections: List[Tuple[str, str]],
        required_services: Set[str],
        optional_services: Set[str]
    ) -> Tuple[bool, str, List[str]]:
        """
        Validate an architecture against level-specific requirements.
        
        Args:
            level_id: ID of the level
            services: List of service IDs in the architecture
            connections: List of connections between services
            required_services: Set of required services for the level
            optional_services: Set of optional services for the level
            
        Returns:
            Tuple of (is_valid, message, issues)
        """
        # Check if all required services are present
        missing_services = required_services - set(services)
        if missing_services:
            return (
                False,
                f"Missing required services: {', '.join(missing_services)}",
                [f"Missing: {service}" for service in missing_services]
            )
        
        # Check for level-specific requirements
        if level_id == 1:
            return cls._validate_level1(services, connections)
        elif level_id == 2:
            return cls._validate_level2(services, connections)
        elif level_id == 3:
            return cls._validate_level3(services, connections)
        elif level_id == 4:
            return cls._validate_level4(services, connections)
        elif level_id == 5:
            return cls._validate_level5(services, connections)
        elif level_id == 6:
            return cls._validate_level6(services, connections)
        elif level_id == 7:
            return cls._validate_level7(services, connections)
        elif level_id == 8:
            return cls._validate_level8(services, connections)
        elif level_id == 9:
            return cls._validate_level9(services, connections)
        elif level_id == 10:
            return cls._validate_level10(services, connections)
        
        # Default validation for unknown levels
        return (True, "Architecture meets basic requirements", [])
    
    @classmethod
    def _validate_level1(cls, services: List[str], connections: List[Tuple[str, str]]) -> Tuple[bool, str, List[str]]:
        """
        Validate Level 1: Blog API architecture.
        
        Args:
            services: List of service IDs in the architecture
            connections: List of connections between services
            
        Returns:
            Tuple of (is_valid, message, issues)
        """
        issues = []
        
        # Check for API Gateway to Lambda connection
        if not cls._has_connection("api_gateway", "lambda", connections):
            issues.append("API Gateway must be connected to Lambda for request processing")
        
        # Check for Lambda to DynamoDB connection
        if not cls._has_connection("lambda", "dynamodb", connections):
            issues.append("Lambda must be connected to DynamoDB for data storage")
        
        # Check for Lambda to S3 connection
        if not cls._has_connection("lambda", "s3", connections):
            issues.append("Lambda must be connected to S3 for media storage")
        
        # Check for IAM role if present
        if "iam" in services and not cls._has_connection("iam", "lambda", connections):
            issues.append("IAM role must be connected to Lambda for permissions")
        
        if issues:
            return (False, f"Architecture issue: {issues[0]}", issues)
        
        return (True, "Blog API architecture validated successfully!", [])
    
    @classmethod
    def _validate_level2(cls, services: List[str], connections: List[Tuple[str, str]]) -> Tuple[bool, str, List[str]]:
        """
        Validate Level 2: Static Portfolio Site architecture.
        
        Args:
            services: List of service IDs in the architecture
            connections: List of connections between services
            
        Returns:
            Tuple of (is_valid, message, issues)
        """
        issues = []
        
        # Check for CloudFront to S3 connection
        if not cls._has_connection("cloudfront", "s3", connections):
            issues.append("CloudFront must be connected to S3 for content delivery")
        
        # Check for WAF if present
        if "waf" in services and not cls._has_connection("waf", "cloudfront", connections):
            issues.append("WAF must be connected to CloudFront for protection")
        
        # Check for Lambda if present
        if "lambda" in services and not cls._has_connection("lambda", "s3", connections):
            issues.append("Lambda should be connected to S3 for dynamic content")
        
        if issues:
            return (False, f"Architecture issue: {issues[0]}", issues)
        
        return (True, "Static Portfolio Site architecture validated successfully!", [])
    
    @classmethod
    def _validate_level3(cls, services: List[str], connections: List[Tuple[str, str]]) -> Tuple[bool, str, List[str]]:
        """
        Validate Level 3: Secure User Authentication architecture.
        
        Args:
            services: List of service IDs in the architecture
            connections: List of connections between services
            
        Returns:
            Tuple of (is_valid, message, issues)
        """
        issues = []
        
        # Check for Cognito to API Gateway connection
        if not cls._has_connection("cognito", "api_gateway", connections):
            issues.append("Cognito must be connected to API Gateway for authentication")
        
        # Check for API Gateway to Lambda connection
        if not cls._has_connection("api_gateway", "lambda", connections):
            issues.append("API Gateway must be connected to Lambda for processing")
        
        # Check for Lambda to Secrets Manager connection
        if not cls._has_connection("lambda", "secrets_manager", connections):
            issues.append("Lambda must be connected to Secrets Manager for secure credentials")
        
        if issues:
            return (False, f"Architecture issue: {issues[0]}", issues)
        
        return (True, "Secure User Authentication architecture validated successfully!", [])
    
    @classmethod
    def _validate_level4(cls, services: List[str], connections: List[Tuple[str, str]]) -> Tuple[bool, str, List[str]]:
        """
        Validate Level 4: Real-time Chat Service architecture.
        
        Args:
            services: List of service IDs in the architecture
            connections: List of connections between services
            
        Returns:
            Tuple of (is_valid, message, issues)
        """
        issues = []
        
        # Check for API Gateway to Lambda connection
        if not cls._has_connection("api_gateway", "lambda", connections):
            issues.append("API Gateway must be connected to Lambda for WebSocket handling")
        
        # Check for Lambda to SQS connection
        if not cls._has_connection("lambda", "sqs", connections):
            issues.append("Lambda must be connected to SQS for message queuing")
        
        # Check for Lambda to SNS connection
        if not cls._has_connection("lambda", "sns", connections):
            issues.append("Lambda must be connected to SNS for notifications")
        
        # Check for Lambda to DynamoDB connection
        if not cls._has_connection("lambda", "dynamodb", connections):
            issues.append("Lambda must be connected to DynamoDB for message storage")
        
        if issues:
            return (False, f"Architecture issue: {issues[0]}", issues)
        
        return (True, "Real-time Chat Service architecture validated successfully!", [])
    
    @classmethod
    def _validate_level5(cls, services: List[str], connections: List[Tuple[str, str]]) -> Tuple[bool, str, List[str]]:
        """
        Validate Level 5: IoT Data Pipeline architecture.
        
        Args:
            services: List of service IDs in the architecture
            connections: List of connections between services
            
        Returns:
            Tuple of (is_valid, message, issues)
        """
        issues = []
        
        # Check for Kinesis to Lambda connection
        if not cls._has_connection("kinesis", "lambda", connections):
            issues.append("Kinesis must be connected to Lambda for data processing")
        
        # Check for Lambda to S3 connection
        if not cls._has_connection("lambda", "s3", connections):
            issues.append("Lambda must be connected to S3 for data storage")
        
        # Check for S3 to Redshift connection or Lambda to Redshift connection
        if not (cls._has_connection("s3", "redshift", connections) or cls._has_connection("lambda", "redshift", connections)):
            issues.append("Either S3 or Lambda must be connected to Redshift for data warehousing")
        
        if issues:
            return (False, f"Architecture issue: {issues[0]}", issues)
        
        return (True, "IoT Data Pipeline architecture validated successfully!", [])
    
    @classmethod
    def _validate_level6(cls, services: List[str], connections: List[Tuple[str, str]]) -> Tuple[bool, str, List[str]]:
        """
        Validate Level 6: High-Volume Payment System architecture.
        
        Args:
            services: List of service IDs in the architecture
            connections: List of connections between services
            
        Returns:
            Tuple of (is_valid, message, issues)
        """
        issues = []
        
        # Check for VPC to EC2 connection
        if not cls._has_connection("vpc", "ec2", connections):
            issues.append("EC2 instances must be in a VPC")
        
        # Check for VPC to RDS connection
        if not cls._has_connection("vpc", "rds", connections):
            issues.append("RDS must be in a VPC")
        
        # Check for Auto Scaling to EC2 connection
        if not cls._has_connection("auto_scaling", "ec2", connections):
            issues.append("Auto Scaling must be connected to EC2 for scalability")
        
        # Check for ALB to EC2 connection
        if not cls._has_connection("alb", "ec2", connections):
            issues.append("ALB must be connected to EC2 for load balancing")
        
        if issues:
            return (False, f"Architecture issue: {issues[0]}", issues)
        
        return (True, "High-Volume Payment System architecture validated successfully!", [])
    
    @classmethod
    def _validate_level7(cls, services: List[str], connections: List[Tuple[str, str]]) -> Tuple[bool, str, List[str]]:
        """
        Validate Level 7: HIPAA Compliant Healthcare API architecture.
        
        Args:
            services: List of service IDs in the architecture
            connections: List of connections between services
            
        Returns:
            Tuple of (is_valid, message, issues)
        """
        issues = []
        
        # Check for WAF to API Gateway connection
        if not cls._has_connection("waf", "api_gateway", connections):
            issues.append("WAF must be connected to API Gateway for protection")
        
        # Check for API Gateway to Lambda connection
        if not cls._has_connection("api_gateway", "lambda", connections):
            issues.append("API Gateway must be connected to Lambda for processing")
        
        # Check for Lambda to DynamoDB connection
        if not cls._has_connection("lambda", "dynamodb", connections):
            issues.append("Lambda must be connected to DynamoDB for data storage")
        
        # Check for KMS to DynamoDB connection
        if not cls._has_connection("kms", "dynamodb", connections):
            issues.append("KMS must be connected to DynamoDB for encryption")
        
        # Check for CloudTrail connection
        if not any(source == "cloudtrail" for source, _ in connections):
            issues.append("CloudTrail must be connected for audit logging")
        
        if issues:
            return (False, f"Architecture issue: {issues[0]}", issues)
        
        return (True, "HIPAA Compliant Healthcare API architecture validated successfully!", [])
    
    @classmethod
    def _validate_level8(cls, services: List[str], connections: List[Tuple[str, str]]) -> Tuple[bool, str, List[str]]:
        """
        Validate Level 8: Video CDN and Transcoding architecture.
        
        Args:
            services: List of service IDs in the architecture
            connections: List of connections between services
            
        Returns:
            Tuple of (is_valid, message, issues)
        """
        issues = []
        
        # Check for S3 to MediaConvert connection or Lambda to MediaConvert connection
        if not (cls._has_connection("s3", "media_convert", connections) or cls._has_connection("lambda", "media_convert", connections)):
            issues.append("Either S3 or Lambda must be connected to MediaConvert for transcoding")
        
        # Check for MediaConvert to S3 connection
        if not cls._has_connection("media_convert", "s3", connections):
            issues.append("MediaConvert must be connected to S3 for output storage")
        
        # Check for CloudFront to S3 connection
        if not cls._has_connection("cloudfront", "s3", connections):
            issues.append("CloudFront must be connected to S3 for content delivery")
        
        # Check for Lambda connection for workflow orchestration
        if not any(target == "lambda" for _, target in connections):
            issues.append("Lambda must be used for workflow orchestration")
        
        if issues:
            return (False, f"Architecture issue: {issues[0]}", issues)
        
        return (True, "Video CDN and Transcoding architecture validated successfully!", [])
    
    @classmethod
    def _validate_level9(cls, services: List[str], connections: List[Tuple[str, str]]) -> Tuple[bool, str, List[str]]:
        """
        Validate Level 9: Microservices Architecture.
        
        Args:
            services: List of service IDs in the architecture
            connections: List of connections between services
            
        Returns:
            Tuple of (is_valid, message, issues)
        """
        issues = []
        
        # Check for ECS or EKS
        if "ecs" not in services and "eks" not in services:
            issues.append("Either ECS or EKS must be used for container orchestration")
        
        # Check for App Mesh connection
        if not any(source == "app_mesh" for source, _ in connections):
            issues.append("App Mesh must be used for service mesh")
        
        # Check for ALB connection
        if not any(source == "alb" for source, _ in connections):
            issues.append("ALB must be used for load balancing")
        
        # Check for DynamoDB connection
        if not any(target == "dynamodb" for _, target in connections):
            issues.append("DynamoDB must be used for product catalog")
        
        # Check for S3 connection
        if not any(target == "s3" for _, target in connections):
            issues.append("S3 must be used for static assets")
        
        if issues:
            return (False, f"Architecture issue: {issues[0]}", issues)
        
        return (True, "Microservices Architecture validated successfully!", [])
    
    @classmethod
    def _validate_level10(cls, services: List[str], connections: List[Tuple[str, str]]) -> Tuple[bool, str, List[str]]:
        """
        Validate Level 10: Secure FinTech Platform architecture.
        
        Args:
            services: List of service IDs in the architecture
            connections: List of connections between services
            
        Returns:
            Tuple of (is_valid, message, issues)
        """
        issues = []
        
        # Check for CloudHSM for key management
        if not any(source == "cloudhsm" for source, _ in connections):
            issues.append("CloudHSM must be used for key management")
        
        # Check for GuardDuty for threat detection
        if not any(source == "guardduty" for source, _ in connections):
            issues.append("GuardDuty must be used for threat detection")
        
        # Check for Macie for data protection
        if not any(source == "macie" for source, _ in connections):
            issues.append("Macie must be used for data protection")
        
        # Check for VPC to RDS connection
        if not cls._has_connection("vpc", "rds", connections):
            issues.append("RDS must be in a VPC")
        
        # Check for VPC to EC2 connection
        if not cls._has_connection("vpc", "ec2", connections):
            issues.append("EC2 instances must be in a VPC")
        
        # Check for ALB to EC2 connection
        if not cls._has_connection("alb", "ec2", connections):
            issues.append("ALB must be connected to EC2 for load balancing")
        
        if issues:
            return (False, f"Architecture issue: {issues[0]}", issues)
        
        return (True, "Secure FinTech Platform architecture validated successfully!", [])
    
    @staticmethod
    def _has_connection(source: str, target: str, connections: List[Tuple[str, str]]) -> bool:
        """
        Check if there is a connection between source and target.
        
        Args:
            source: Source service ID
            target: Target service ID
            connections: List of connections between services
            
        Returns:
            True if connection exists, False otherwise
        """
        return (source, target) in connections