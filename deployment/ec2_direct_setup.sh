#!/bin/bash
# Direct EC2 Setup (No Docker) for Research Paper Analyzer

# Update system
sudo yum update -y

# Install Python 3.12
sudo yum install python3.12 python3.12-pip git -y

# Clone repository
cd /home/ec2-user
git clone https://github.com/yourusername/research-paper-analyzer.git
cd research-paper-analyzer

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
NVIDIA_API_KEY=your_key_here
EOF

# Install and configure systemd service
sudo tee /etc/systemd/system/research-app.service > /dev/null <<EOF
[Unit]
Description=Research Paper Analyzer
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/research-paper-analyzer
Environment="PATH=/home/ec2-user/research-paper-analyzer/venv/bin"
ExecStart=/home/ec2-user/research-paper-analyzer/venv/bin/streamlit run app.py --server.port=80 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start the service
sudo systemctl daemon-reload
sudo systemctl enable research-app
sudo systemctl start research-app

echo "✅ Deployment complete! App running on port 80"