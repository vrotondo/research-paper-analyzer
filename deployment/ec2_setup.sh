#!/bin/bash
# AWS EC2 Setup Script for Research Paper Analyzer

# Update system
sudo yum update -y

# Install Docker
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository (replace with your repo)
cd /home/ec2-user
git clone https://github.com/yourusername/research-paper-analyzer.git
cd research-paper-analyzer

# Create .env file
cat > .env << EOF
NVIDIA_API_KEY=your_key_here
EOF

# Build and run
docker build -t research-paper-analyzer .
docker run -d -p 80:8501 --env-file .env --name research-app research-paper-analyzer

echo "✅ Deployment complete! App running on port 80"