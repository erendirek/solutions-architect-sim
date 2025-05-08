# Solutions Architect Simulator - Level Design (Continued)

## Level 6: High-Volume Payment System

**Scenario**: Design a high-volume payment processing system for a FinTech company.

**Requirements**:
- RDS (Aurora) for transactional data
- VPC for network isolation
- EC2 for application servers
- Auto Scaling for handling traffic spikes
- ALB for load balancing

**Optional Services**:
- CloudWatch for monitoring
- SNS for alerts
- Lambda for event processing
- SQS for transaction queuing

**Budget**: $300/month
**Max Latency**: 100ms

## Level 7: HIPAA Compliant Healthcare API

**Scenario**: Create a HIPAA compliant API for a healthcare application that stores and processes patient data.

**Requirements**:
- API Gateway for API access
- Lambda for processing
- DynamoDB for patient data
- KMS for encryption
- CloudTrail for audit logging
- WAF for API protection

**Optional Services**:
- VPC for network isolation
- S3 for document storage
- SNS for notifications
- CloudWatch for monitoring

**Budget**: $250/month
**Max Latency**: 200ms

## Level 8: Video CDN and Transcoding

**Scenario**: Build a video content delivery network with on-the-fly transcoding for different device formats.

**Requirements**:
- MediaConvert for video transcoding
- S3 for video storage
- CloudFront for content delivery
- Lambda for workflow orchestration

**Optional Services**:
- Elastic Transcoder (alternative to MediaConvert)
- SNS for notifications
- SQS for job queuing
- DynamoDB for metadata

**Budget**: $350/month
**Max Latency**: 400ms

## Level 9: Microservices Architecture

**Scenario**: Design a microservices architecture for a complex e-commerce application.

**Requirements**:
- ECS for container orchestration
- App Mesh for service mesh
- ALB for load balancing
- DynamoDB for product catalog
- S3 for static assets

**Optional Services**:
- EKS as alternative to ECS
- CloudWatch for monitoring
- SNS for notifications
- SQS for message queuing
- Lambda for event processing

**Budget**: $400/month
**Max Latency**: 150ms

## Level 10: Secure FinTech Platform

**Scenario**: Design a highly secure platform for a financial technology company that handles sensitive customer data and transactions.

**Requirements**:
- CloudHSM for hardware security modules
- GuardDuty for threat detection
- Macie for data protection
- VPC for network isolation
- RDS for transactional data
- EC2 for application servers
- ALB for load balancing

**Optional Services**:
- WAF for web application firewall
- CloudTrail for audit logging
- KMS for encryption
- Secrets Manager for credential management
- Cognito for user authentication

**Budget**: $500/month
**Max Latency**: 120ms