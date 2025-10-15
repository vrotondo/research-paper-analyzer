# AWS EC2 Deployment Guide

## Prerequisites
- AWS Account
- GitHub repository with your code
- EC2 key pair (.pem file)

## Quick Deployment Steps

### 1. Push Code to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Launch EC2 Instance

**Via AWS Console:**
1. Go to [AWS EC2 Console](https://console.aws.amazon.com/ec2/)
2. Click **"Launch Instance"**
3. Configure:
   - **Name**: `research-paper-analyzer`
   - **AMI**: Amazon Linux 2023 AMI
   - **Instance Type**: t3.medium (2 vCPU, 4 GB RAM)
   - **Key pair**: Select/create a key pair
   - **Security Group**: Configure as shown below
4. Click **"Launch Instance"**

**Security Group Settings:**
- **SSH (22)**: Your IP only
- **Custom TCP (8501)**: 0.0.0.0/0 (Anywhere)
- **HTTP (80)**: 0.0.0.0/0 (optional, for future)

### 3. Connect to EC2
```bash
# Change permissions on your key
chmod 400 your-key.pem

# Connect to EC2
ssh -i "your-key.pem" ec2-user@your-ec2-public-ip
```

### 4. Run Deployment Script
```bash
# Download the setup script
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/research-paper-analyzer/main/deployment/ec2_setup.sh

# Make it executable
chmod +x ec2_setup.sh

# Run it
./ec2_setup.sh
```

**Or manually run commands:**
```bash
sudo yum update -y
sudo yum install python3.12 python3.12-pip git -y
cd /home/ec2-user
git clone https://github.com/YOUR_USERNAME/research-paper-analyzer.git
cd research-paper-analyzer
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Create .env file with your API key
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

### 5. Access Your App

Open browser and go to:
```
http://your-ec2-public-ip:8501
```

## Managing the Service
```bash
# Check if running
sudo systemctl status research-app

# View live logs
sudo journalctl -u research-app -f

# Restart
sudo systemctl restart research-app

# Stop
sudo systemctl stop research-app

# Start
sudo systemctl start research-app
```

## Updating the App
```bash
cd /home/ec2-user/research-paper-analyzer
git pull origin main
sudo systemctl restart research-app
```

## Troubleshooting

### App not accessible
- Check security group allows port 8501
- Verify service is running: `sudo systemctl status research-app`
- Check logs: `sudo journalctl -u research-app -n 50`

### Service fails to start
- Check Python version: `python3.12 --version`
- Verify virtual environment: `source venv/bin/activate && python --version`
- Check permissions: `ls -la /home/ec2-user/research-paper-analyzer`

### Out of memory
- Upgrade to t3.large (8 GB RAM)
- Monitor with: `free -h` and `top`

## Cost Estimate

- **t3.medium**: ~$0.04/hour (~$30/month)
- **Data transfer**: Free tier covers most usage
- **Storage**: 8 GB EBS included in free tier

Stop instance when not in use to save costs!

## Security Best Practices

1. **Restrict SSH**: Only allow your IP in security group
2. **Update regularly**: `sudo yum update -y`
3. **Use HTTPS**: Add SSL certificate (Let's Encrypt) for production
4. **Rotate API keys**: Don't commit keys to GitHub
5. **Firewall**: Keep security group rules minimal