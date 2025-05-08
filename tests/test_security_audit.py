"""
Unit tests for the security audit module.
"""
import unittest
from typing import List, Tuple

from tests.security_audit import SecurityAudit


class TestSecurityAudit(unittest.TestCase):
    """Test cases for the SecurityAudit class."""
    
    def test_unencrypted_s3(self) -> None:
        """Test detection of unencrypted S3 buckets."""
        services = ["s3", "lambda", "api_gateway"]
        connections = [("api_gateway", "lambda"), ("lambda", "s3")]
        
        issues = SecurityAudit.audit_architecture(services, connections)
        
        self.assertIn("S3 bucket is not encrypted with KMS", issues)
    
    def test_encrypted_s3(self) -> None:
        """Test that encrypted S3 buckets pass the audit."""
        services = ["s3", "lambda", "api_gateway", "kms"]
        connections = [("api_gateway", "lambda"), ("lambda", "s3"), ("kms", "s3")]
        
        issues = SecurityAudit.audit_architecture(services, connections)
        
        self.assertNotIn("S3 bucket is not encrypted with KMS", issues)
    
    def test_public_s3_without_cloudfront(self) -> None:
        """Test detection of public S3 buckets without CloudFront."""
        services = ["s3", "api_gateway"]
        connections = [("api_gateway", "s3")]
        
        issues = SecurityAudit.audit_architecture(services, connections)
        
        self.assertIn("S3 bucket is publicly accessible without CloudFront", issues)
    
    def test_s3_with_cloudfront(self) -> None:
        """Test that S3 with CloudFront passes the audit."""
        services = ["s3", "cloudfront"]
        connections = [("cloudfront", "s3")]
        
        issues = SecurityAudit.audit_architecture(services, connections)
        
        self.assertNotIn("S3 bucket is publicly accessible without CloudFront", issues)
    
    def test_lambda_without_iam(self) -> None:
        """Test detection of Lambda functions without IAM roles."""
        services = ["lambda", "api_gateway"]
        connections = [("api_gateway", "lambda")]
        
        issues = SecurityAudit.audit_architecture(services, connections)
        
        self.assertIn("Lambda function without IAM role", issues)
    
    def test_lambda_with_iam(self) -> None:
        """Test that Lambda with IAM passes the audit."""
        services = ["lambda", "api_gateway", "iam"]
        connections = [("api_gateway", "lambda"), ("iam", "lambda")]
        
        issues = SecurityAudit.audit_architecture(services, connections)
        
        self.assertNotIn("Lambda function without IAM role", issues)
    
    def test_rds_without_vpc(self) -> None:
        """Test detection of RDS without VPC."""
        services = ["rds", "ec2"]
        connections = [("ec2", "rds")]
        
        issues = SecurityAudit.audit_architecture(services, connections)
        
        self.assertIn("RDS database is not in a VPC", issues)
    
    def test_rds_with_vpc(self) -> None:
        """Test that RDS with VPC passes the audit."""
        services = ["rds", "ec2", "vpc"]
        connections = [("ec2", "rds"), ("vpc", "rds")]
        
        issues = SecurityAudit.audit_architecture(services, connections)
        
        self.assertNotIn("RDS database is not in a VPC", issues)


if __name__ == "__main__":
    unittest.main()