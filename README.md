
# TNFS Monitor

Andrew Diller @dillera
with help from chatGPT

----


TNFS Monitor is a Flask application that monitors the status of servers, specifically checking TCP and UDP connectivity on port 16384. This application provides both an admin interface for managing servers and a view-only page for monitoring server status.

## Features

- Monitor TCP and UDP connectivity on port 16384 for multiple servers.
- View real-time status with dynamic updates in the browser.
- Admin interface for adding, editing, and deleting monitored servers.
- Customizable polling period with a countdown timer on the view-only page.
- Automatically refreshes the status page when the countdown reaches zero.
- Visual indicators for server status using icons for "Up" and "Down".
- Easily deploy as a systemd service for reliable and consistent operation.

## Prerequisites

- **Python 3.6+**
- **pip** (Python package installer)
- **virtualenv** (Optional but recommended for isolated environments)
- **systemd** (For managing the Flask application as a service)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/dillera/tnfs-monitor.git
cd tnfs-monitor
```

### Step 2: Set Up the Virtual Environment

It’s recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Install the required Python packages using pip.

```bash
pip install -r requirements.txt
```

### Step 4: Set Up the Database

Initialize the SQLite database.

```bash
export FLASK_APP=app:create_app
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Running the Application

### Option 1: Run Locally

You can run the Flask application locally for development purposes.

```bash
export FLASK_APP=app:create_app
export FLASK_ENV=development
flask run
```

Access the application at `http://127.0.0.1:5000/`.

### Option 2: Run as a Systemd Service

To ensure the application runs automatically at startup and is managed by systemd, follow these steps.

#### Step 1: Run the Setup Script

A helper script is provided to set up the Flask app as a systemd service.

```bash
./setup_flask_systemd.sh /full/path/to/your/app
```

Replace `/full/path/to/your/app` with the actual path where the application is located.

#### Step 2: Access the Application

Once the service is running, access the application at `http://<your-server-ip>:8000/`.

## Systemd Service Management

Once set up as a systemd service, you can manage the Flask app using the following commands:

- **Start the service**: `sudo systemctl start tnfs-monitor.service`
- **Stop the service**: `sudo systemctl stop tnfs-monitor.service`
- **Restart the service**: `sudo systemctl restart tnfs-monitor.service`
- **Check the status**: `sudo systemctl status tnfs-monitor.service`
- **Enable the service to start on boot**: `sudo systemctl enable tnfs-monitor.service`

## Application Features

### Admin Page

- **Add Servers**: Add new servers to monitor.
- **Edit/Delete Servers**: Manage existing servers.
- **Set Polling Period**: Configure the polling interval in seconds.

### View Servers Page

- **Server Status**: Displays the status of all monitored servers with real-time updates.
- **Countdown Timer**: Automatically refreshes the page when the countdown reaches zero, showing the latest status.
- **Visual Status Indicators**: Green arrows indicate "Up", red arrows indicate "Down".
- **Last Checked**: Displays the last checked date in `MM/DD/YY` format.
- **Time Since Last Check**: Displays the time in seconds since the last check.

## Application Structure

```
tnfs-monitor/
│
├── app/
│   ├── __init__.py        # Flask app factory
│   ├── models.py          # Database models
│   ├── routes.py          # Application routes
│   ├── templates/         # HTML templates
│   │   ├── base.html      # Base template
│   │   ├── view_servers.html # View-only page template
│   │   └── admin.html     # Admin page template
│   └── static/            # Static files (CSS, JS)
│       └── style.css      # Application styles
│
├── monitor.py             # Script for periodic server checks
├── setup_flask_systemd.sh # Helper script to set up systemd service
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Contributing

If you’d like to contribute to this project, feel free to fork the repository and submit a pull request. Contributions are welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
