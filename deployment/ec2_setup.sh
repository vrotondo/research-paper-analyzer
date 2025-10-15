#!/bin/bash
# Direct EC2 Setup for Research Paper Analyzer
# No Docker required!

set -e  # Exit on any error

echo "🚀 Starting deployment..."

# Update system
echo "📦 Updating system packages..."
sudo yum update -y

# Install Python 3.12 and git
echo "🐍 Installing Python 3.12..."
sudo yum install python3.12 python3.12-pip git -y

# Clone repository (you'll update this URL)
echo "📥 Cloning repository..."
cd /home/ec2-user

# If directory exists, remove it (for redeployment)
if [ -d "research-paper-analyzer" ]; then
    rm -rf research-paper-analyzer
fi

git clone https://github.com/vrotondo/research-paper-analyzer.git
cd research-paper-analyzer

# Create virtual environment
echo "🔧 Setting up virtual environment..."
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file with API key
echo "🔑 Setting up environment variables..."
cat > .env << 'EOF'
NVIDIA_API_KEY=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
EOF

# Create data directories
mkdir -p data/raw data/processed

# Create systemd service file
echo "⚙️ Creating system service..."
sudo tee /etc/systemd/system/research-app.service > /dev/null <<'EOF'
[Unit]
Description=Research Paper Analyzer
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/research-paper-analyzer
Environment="PATH=/home/ec2-user/research-paper-analyzer/venv/bin"
ExecStart=/home/ec2-user/research-paper-analyzer/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start service
echo "🎬 Starting application..."
sudo systemctl daemon-reload
sudo systemctl enable research-app
sudo systemctl start research-app

# Wait a moment for service to start
sleep 3

# Check status
echo ""
echo "📊 Service status:"
sudo systemctl status research-app --no-pager

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Your app should be accessible at:"
echo "   http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8501"
echo ""
echo "📝 Useful commands:"
echo "   Check logs: sudo journalctl -u research-app -f"
echo "   Restart app: sudo systemctl restart research-app"
echo "   Stop app: sudo systemctl stop research-app"