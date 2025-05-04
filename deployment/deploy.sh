#!/bin/bash
# Production deployment script for BitNet_LLM_Virtual_Coworker_Builder

set -e  # Exit on error

# Configuration
APP_NAME="bitnet-vc-builder"
DEPLOY_DIR="/opt/$APP_NAME"
LOG_DIR="/var/log/$APP_NAME"
CONFIG_DIR="/etc/$APP_NAME"
DATA_DIR="/var/lib/$APP_NAME"
USER="$APP_NAME"
GROUP="$APP_NAME"
VENV_DIR="$DEPLOY_DIR/venv"
REPO_URL="https://github.com/ai-in-pm/BitNet-LLM-Virtual-Coworker-Builder.git"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --branch)
      BRANCH="$2"
      shift 2
      ;;
    --config)
      CONFIG_FILE="$2"
      shift 2
      ;;
    --help)
      echo "Usage: $0 [options]"
      echo "Options:"
      echo "  --branch BRANCH    Git branch to deploy (default: main)"
      echo "  --config FILE      Configuration file to use (default: production.yaml)"
      echo "  --help             Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Set defaults
BRANCH=${BRANCH:-main}
CONFIG_FILE=${CONFIG_FILE:-production.yaml}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

echo "=== BitNet Virtual Co-worker Builder Deployment ==="
echo "Branch: $BRANCH"
echo "Config: $CONFIG_FILE"
echo "=================================================="

# Create user and group if they don't exist
if ! getent group $GROUP > /dev/null; then
  echo "Creating group $GROUP..."
  groupadd $GROUP
fi

if ! id -u $USER > /dev/null 2>&1; then
  echo "Creating user $USER..."
  useradd -m -g $GROUP -s /bin/bash $USER
fi

# Create directories
echo "Creating directories..."
mkdir -p $DEPLOY_DIR
mkdir -p $LOG_DIR
mkdir -p $CONFIG_DIR
mkdir -p $DATA_DIR
mkdir -p $DATA_DIR/models
mkdir -p $DATA_DIR/cache
mkdir -p $DATA_DIR/memory

# Set permissions
chown -R $USER:$GROUP $DEPLOY_DIR
chown -R $USER:$GROUP $LOG_DIR
chown -R $USER:$GROUP $CONFIG_DIR
chown -R $USER:$GROUP $DATA_DIR

# Clone or update repository
if [ -d "$DEPLOY_DIR/repo" ]; then
  echo "Updating repository..."
  cd $DEPLOY_DIR/repo
  sudo -u $USER git fetch --all
  sudo -u $USER git checkout $BRANCH
  sudo -u $USER git pull
else
  echo "Cloning repository..."
  sudo -u $USER git clone $REPO_URL $DEPLOY_DIR/repo
  cd $DEPLOY_DIR/repo
  sudo -u $USER git checkout $BRANCH
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  sudo -u $USER python3 -m venv $VENV_DIR
fi

# Install dependencies
echo "Installing dependencies..."
sudo -u $USER $VENV_DIR/bin/pip install --upgrade pip
sudo -u $USER $VENV_DIR/bin/pip install -e $DEPLOY_DIR/repo[ui]

# Copy configuration
echo "Copying configuration..."
cp $DEPLOY_DIR/repo/config/$CONFIG_FILE $CONFIG_DIR/config.yaml
chown $USER:$GROUP $CONFIG_DIR/config.yaml

# Create systemd service for API server
echo "Creating systemd service for API server..."
cat > /etc/systemd/system/$APP_NAME-api.service << EOF
[Unit]
Description=BitNet Virtual Co-worker Builder API Server
After=network.target

[Service]
User=$USER
Group=$GROUP
WorkingDirectory=$DEPLOY_DIR/repo
Environment="PATH=$VENV_DIR/bin:/usr/local/bin:/usr/bin:/bin"
Environment="CONFIG_PATH=$CONFIG_DIR/config.yaml"
Environment="PYTHONPATH=$DEPLOY_DIR/repo"
ExecStart=$VENV_DIR/bin/python -m bitnet_vc_builder.api.server --config \$CONFIG_PATH
Restart=always
RestartSec=5
StandardOutput=append:$LOG_DIR/api.log
StandardError=append:$LOG_DIR/api.error.log

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for Web UI
echo "Creating systemd service for Web UI..."
cat > /etc/systemd/system/$APP_NAME-ui.service << EOF
[Unit]
Description=BitNet Virtual Co-worker Builder Web UI
After=network.target $APP_NAME-api.service

[Service]
User=$USER
Group=$GROUP
WorkingDirectory=$DEPLOY_DIR/repo
Environment="PATH=$VENV_DIR/bin:/usr/local/bin:/usr/bin:/bin"
Environment="CONFIG_PATH=$CONFIG_DIR/config.yaml"
Environment="PYTHONPATH=$DEPLOY_DIR/repo"
ExecStart=$VENV_DIR/bin/python -m bitnet_vc_builder.ui.web.app --config \$CONFIG_PATH
Restart=always
RestartSec=5
StandardOutput=append:$LOG_DIR/ui.log
StandardError=append:$LOG_DIR/ui.error.log

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
echo "Reloading systemd..."
systemctl daemon-reload

# Enable and start services
echo "Enabling and starting services..."
systemctl enable $APP_NAME-api.service
systemctl enable $APP_NAME-ui.service
systemctl start $APP_NAME-api.service
systemctl start $APP_NAME-ui.service

# Check service status
echo "Checking service status..."
systemctl status $APP_NAME-api.service
systemctl status $APP_NAME-ui.service

echo "=== Deployment Complete ==="
echo "API Server: http://localhost:8000"
echo "Web UI: http://localhost:8501"
echo "Logs: $LOG_DIR"
echo "Configuration: $CONFIG_DIR/config.yaml"
echo "=========================="
