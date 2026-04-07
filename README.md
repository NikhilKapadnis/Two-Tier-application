# 🚀 Two-Tier Flask Application on AWS

A production-style **two-tier web application** built using **Flask (Python)** and **PostgreSQL**, deployed on AWS using:

- **Amazon ECS (Fargate)** for container orchestration  
- **Amazon RDS (PostgreSQL)** for the database  
- **Application Load Balancer (ALB)** for traffic routing  
- **Amazon ECR** for container image storage  
- **GitHub Actions** for CI/CD automation  

---

## 🏗️ Architecture Overview

```text
                🌐 User (Browser)
                       │
                       ▼
        ┌────────────────────────────┐
        │  Application Load Balancer │
        │      (Public Subnets)      │
        └────────────┬──────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │   ECS Fargate Service      │
        │    (Private Subnets)       │
        │                            │
        │  Flask App Container       │
        │     Port: 5000             │
        └────────────┬──────────────┘
                     │

⚙️ Deployment Flow (CI/CD):


GitHub Push
    ↓
GitHub Actions
    ↓
Docker Image Build
    ↓
Push to Amazon ECR
    ↓
Update ECS Task Definition
    ↓
ECS Service Deploys New Container
    ↓
ALB Routes Traffic to Updated Version
                     ▼
        ┌────────────────────────────┐
        │   Amazon RDS PostgreSQL    │
        │    (Private Subnets)       │
        │     Port: 5432             │
        └────────────────────────────┘

💡 Why This Architecture? 
Scalable → ECS Fargate handles scaling without managing servers
Secure → ECS and RDS are in private subnets
Reliable → ALB performs health checks and routing
Automated → CI/CD pipeline handles deployments
Production-ready pattern → Common real-world cloud setup
