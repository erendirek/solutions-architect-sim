# Solutions Architect Simulator - Gameplay Guide

This document describes the gameplay mechanics of the Solutions Architect Simulator.

## Game Objective

The objective of the Solutions Architect Simulator is to design AWS architectures that meet specific requirements for different scenarios. Players must select appropriate AWS services, connect them correctly, and ensure the architecture meets security, cost, and performance requirements.

## Game Flow

1. Start the game and select a level from the main menu
2. Choose your game mode (Normal, Tutorial, or Time Trial)
3. Build an architecture that fulfills the level requirements
4. Validate your architecture to complete the level
5. Earn points and a rank based on your solution
6. Return to the main menu to select another level

## Controls

- **Left Mouse Button**: Select services, place them on the canvas, and create connections
- **Hover**: Hover over a service icon to see its description, cost, and latency
- **Validate Button**: Click to validate your architecture and complete the level
- **Menu Button**: Return to the main menu
- **Escape Key**: Return to the main menu

## Main Menu

The main menu allows you to:
- Select any unlocked level
- View level descriptions and requirements
- Toggle Tutorial Mode for levels 1-2
- Toggle Time Trial Mode for any level
- See your completion status and rank for each level

## Building Architectures

1. **Select Services**: Click on a service icon in the left panel
2. **Place Services**: Click on the canvas to place the selected service
3. **Create Connections**: Click on a service, then click on another service to create a connection
4. **Validate**: Click the "Validate Architecture" button to check your solution

## Game Modes

### Normal Mode

Standard gameplay where players build architectures to meet requirements.

### Tutorial Mode

Available for levels 1 and 2, providing step-by-step guidance. To activate:
1. Select level 1 or 2 in the main menu
2. Click the "Tutorial Mode: OFF" button to toggle it to "ON"
3. Click "Start Level"

### Time Trial Mode

Complete the level within 90 seconds for double points. To activate:
1. Select any level in the main menu
2. Click the "Time Trial: OFF" button to toggle it to "ON"
3. Click "Start Level"

## Scoring System

- **Requirements Fulfilled**: +40 points
- **Correct Connection**: +15 points per connection
- **Security Violation**: -30 points per violation
- **Unnecessary Service**: -20 points per service
- **Cost Optimization**: +25 points if under budget

## Ranks

- **Gold Architect**: 250+ points
- **Silver Architect**: 150-249 points
- **Bronze Architect**: <150 points (requires replay)

## Level Progression

Players must complete each level to unlock the next one. Levels increase in complexity:

1. **Blog API**: Simple CRUD API with API Gateway, Lambda, DynamoDB, and S3
2. **Static Portfolio Site**: S3 and CloudFront for content delivery
3. **User Authentication**: Cognito and Secrets Manager
4. **Real-time Chat**: WebSocket API, SQS, SNS
5. **IoT Data Pipeline**: Kinesis, Redshift
6. **Payment System**: RDS, VPC, Auto Scaling
7. **HIPAA Compliance**: KMS, CloudTrail, WAF
8. **Video CDN**: MediaConvert, CloudFront
9. **Microservices**: ECS/EKS, App Mesh
10. **Secure FinTech**: CloudHSM, GuardDuty, Macie