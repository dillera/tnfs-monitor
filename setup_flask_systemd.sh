#!/bin/bash

# Check if the path to the app is provided
if [ -z "$1" ]; then
  echo "Usage: $0 /full/path/to/your/app"
  exit 1
fi

APP_PATH=$1
APP_NAME=$(basename $APP_PATH)
SERVICE_NAME="${APP_NAME}.service"
PYTHON_BIN="$APP_PATH/venv/bin/python"
FLASK_APP="$APP_PATH/app.py"

# Create the systemd service file
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME"

echo "Creating systemd service file at $SERVICE_FILE"

sudo cat <<EOF > $SERVICE_FILE
[Unit]
Description=Gunicorn instance to serve $APP_NAME
After=network.target

[Service]
User=$(whoami)
Group=$(id -gn $(whoami))
WorkingDirectory=$APP_PATH
ExecStart=$PYTHON_BIN -m flask run --host=0.0.0.0 --port=8000

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd to pick up the new service
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable the service to start on boot
echo "Enabling the $SERVICE_NAME service to start on boot..."
sudo systemctl enable $SERVICE_NAME

# Start the service now
echo "Starting the $SERVICE_NAME service..."
sudo systemctl start $SERVICE_NAME

# Check the status of the service
echo "Checking the status of the $SERVICE_NAME service..."
sudo systemctl status $SERVICE_NAME

echo "Setup complete! Your Flask app is now running as a systemd service."