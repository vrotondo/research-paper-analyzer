# AWS Deployment Guide

## Quick Start: EC2 Deployment (Recommended)

### Prerequisites
- AWS Account
- AWS CLI configured
- EC2 key pair created

### Steps

1. **Launch EC2 Instance**
   - AMI: Amazon Linux 2023
   - Instance Type: t3.medium
   - Security Group: Allow ports 22, 80, 8501

2. **Connect and Deploy**
```bash
   ssh -i your-key.pem ec2-user@your-ec2-ip
   
   # Run setup script
   bash deployment/ec2_setup.sh
```

3. **Access Application**
   - URL: `http://your-ec2-public-ip`

### Environment Variables

Create `.env` file:
```
NVIDIA_API_KEY=your_key_here
```

## Alternative: ECS Deployment

See `ecs_deploy.sh` for containerized deployment on AWS ECS Fargate.

## Monitoring

- CloudWatch Logs: `/aws/ec2/research-paper-analyzer`
- Metrics: CPU, Memory, Network

## Cost Estimate

- EC2 t3.medium: ~$0.04/hour (~$30/month)
- ECS Fargate: ~$0.05/hour (~$36/month)

## Troubleshooting

### App not accessible
- Check security group allows port 80/8501
- Verify Docker container is running: `docker ps`

### API errors
- Verify NVIDIA_API_KEY in .env file
- Check API key is valid

### Out of memory
- Upgrade to t3.large (4 GB → 8 GB RAM)