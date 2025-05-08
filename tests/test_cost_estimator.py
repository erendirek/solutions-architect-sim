"""
Unit tests for the cost estimator module.
"""
import unittest
from typing import Dict, List, Tuple
from unittest.mock import patch

from tests.cost_estimator import CostEstimator
from services.service_registry import ServiceInfo, ServiceRegistry


class TestCostEstimator(unittest.TestCase):
    """Test cases for the CostEstimator class."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        # Create mock service info objects
        self.mock_services = {
            "lambda": ServiceInfo(
                service_id="lambda",
                display_name="Lambda",
                description="Serverless compute",
                category="compute",
                icon_path="assets/images/services/lambda.png",
                cost_per_hour=0.0125,
                latency_ms=100.0,
                connection_rules={"direct": ["dynamodb", "s3"]}
            ),
            "dynamodb": ServiceInfo(
                service_id="dynamodb",
                display_name="DynamoDB",
                description="NoSQL database",
                category="database",
                icon_path="assets/images/services/dynamodb.png",
                cost_per_hour=0.05,
                latency_ms=5.0,
                connection_rules={"direct": []}
            ),
            "s3": ServiceInfo(
                service_id="s3",
                display_name="S3",
                description="Object storage",
                category="storage",
                icon_path="assets/images/services/s3.png",
                cost_per_hour=0.01,
                latency_ms=15.0,
                connection_rules={"direct": []}
            )
        }
    
    @patch.object(ServiceRegistry, 'get_service')
    def test_estimate_monthly_cost_single_service(self, mock_get_service) -> None:
        """Test cost estimation for a single service."""
        # Configure the mock
        mock_get_service.side_effect = lambda service_id: self.mock_services.get(service_id)
        
        # Test with a single service
        services = ["lambda"]
        connections = []
        
        expected_cost = self.mock_services["lambda"].cost_per_hour * CostEstimator.HOURS_PER_MONTH
        actual_cost = CostEstimator.estimate_monthly_cost(services, connections)
        
        self.assertAlmostEqual(expected_cost, actual_cost, places=2)
    
    @patch.object(ServiceRegistry, 'get_service')
    def test_estimate_monthly_cost_multiple_services(self, mock_get_service) -> None:
        """Test cost estimation for multiple services."""
        # Configure the mock
        mock_get_service.side_effect = lambda service_id: self.mock_services.get(service_id)
        
        # Test with multiple services
        services = ["lambda", "dynamodb", "s3"]
        connections = [("lambda", "dynamodb"), ("lambda", "s3")]
        
        # Calculate expected cost
        lambda_cost = self.mock_services["lambda"].cost_per_hour * CostEstimator.HOURS_PER_MONTH
        dynamodb_cost = self.mock_services["dynamodb"].cost_per_hour * CostEstimator.HOURS_PER_MONTH
        s3_cost = self.mock_services["s3"].cost_per_hour * CostEstimator.HOURS_PER_MONTH
        
        # Add data transfer costs (2 connections * 5.0 per connection)
        data_transfer_cost = 2 * 5.0
        
        expected_cost = lambda_cost + dynamodb_cost + s3_cost + data_transfer_cost
        actual_cost = CostEstimator.estimate_monthly_cost(services, connections)
        
        self.assertAlmostEqual(expected_cost, actual_cost, places=2)
    
    @patch.object(ServiceRegistry, 'get_service')
    def test_adjust_service_cost(self, mock_get_service) -> None:
        """Test service cost adjustment."""
        # Configure the mock
        mock_get_service.side_effect = lambda service_id: self.mock_services.get(service_id)
        
        # Test Lambda cost adjustment when not connected to API Gateway
        services = ["lambda", "dynamodb"]
        connections = [("lambda", "dynamodb")]
        
        base_cost = 10.0
        adjusted_cost = CostEstimator._adjust_service_cost("lambda", base_cost, services, connections)
        
        # Lambda costs less if not connected to API Gateway
        self.assertAlmostEqual(base_cost * 0.5, adjusted_cost, places=2)


if __name__ == "__main__":
    unittest.main()