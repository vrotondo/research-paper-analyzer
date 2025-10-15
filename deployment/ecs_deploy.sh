#!/bin/bash
# AWS ECS Deployment Script

# Variables
AWS_REGION="us-east-1"
ECR_REPO_NAME="research-paper-analyzer"
ECS_CLUSTER_NAME="research-cluster"
ECS_SERVICE_NAME="research-service"
TASK_FAMILY="research-task"

# 1. Create ECR repository
aws ecr create-repository \
    --repository-name $ECR_REPO_NAME \
    --region $AWS_REGION

# Get ECR URI
ECR_URI=$(aws ecr describe-repositories \
    --repository-names $ECR_REPO_NAME \
    --region $AWS_REGION \
    --query 'repositories[0].repositoryUri' \
    --output text)

# 2. Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI

# 3. Build and push Docker image
docker build -t $ECR_REPO_NAME .
docker tag $ECR_REPO_NAME:latest $ECR_URI:latest
docker push $ECR_URI:latest

# 4. Create ECS Cluster
aws ecs create-cluster \
    --cluster-name $ECS_CLUSTER_NAME \
    --region $AWS_REGION

echo "✅ ECS deployment prepared! Now create task definition in AWS Console"