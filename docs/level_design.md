# Solutions Architect Simulator - Level Design

This document outlines the design for each level in the Solutions Architect Simulator game.

## Level 1: Build a Blog API

**Scenario**: Create a simple blog API that allows users to create, read, update, and delete blog posts.

**Requirements**:
- API Gateway to handle HTTP requests
- Lambda functions to process requests
- DynamoDB to store blog post data
- S3 to store media files

**Optional Services**:
- IAM for proper permissions
- CloudWatch for monitoring

**Budget**: $50/month
**Max Latency**: 300ms

## Level 2: Static Portfolio Site

**Scenario**: Build a static portfolio website with global content delivery.

**Requirements**:
- S3 for static content hosting
- CloudFront for global content delivery

**Optional Services**:
- WAF for security
- Lambda@Edge for customization

**Budget**: $30/month
**Max Latency**: 100ms

## Level 3: Secure User Authentication

**Scenario**: Implement a secure user authentication system for a web application.

**Requirements**:
- Cognito for user authentication
- API Gateway for API access
- Lambda for processing
- Secrets Manager for secure credential storage

**Optional Services**:
- DynamoDB for user data
- S3 for user content
- CloudFront for content delivery

**Budget**: $75/month
**Max Latency**: 250ms

## Level 4: Real-time Chat Service

**Scenario**: Create a real-time chat service that can handle thousands of concurrent users.

**Requirements**:
- WebSocket API Gateway for real-time connections
- Lambda for message processing
- SQS for message queuing
- SNS for notifications
- DynamoDB for message storage

**Optional Services**:
- CloudWatch for monitoring
- IAM for security
- Cognito for user authentication

**Budget**: $100/month
**Max Latency**: 150ms

## Level 5: IoT Data Pipeline

**Scenario**: Build a data pipeline to ingest and analyze IoT sensor data.

**Requirements**:
- Kinesis for data ingestion
- Lambda for data processing
- Redshift for data warehousing
- S3 for data storage

**Optional Services**:
- CloudWatch for monitoring
- SNS for alerts
- DynamoDB for metadata

**Budget**: $200/month
**Max Latency**: 500ms