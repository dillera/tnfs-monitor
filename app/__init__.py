from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import threading
import time
import socket
import datetime
import logging,os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server-status.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)

    # Set up logging
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler("monitor.log"),
                                  logging.StreamHandler()])


    db.init_app(app)
    migrate.init_app(app, db)

    from .models import ServerStatus, Config

    with app.app_context():
        db.create_all()

        ensure_default_config()

        # Start the monitoring thread after the app is fully initialized
        monitoring_thread = threading.Thread(target=monitor_servers, args=(app,))
        monitoring_thread.daemon = True
        monitoring_thread.start()

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app

def ensure_default_config():
    from .models import Config
    if Config.query.first() is None:
        default_config = Config(polling_period=300)
        db.session.add(default_config)
        db.session.commit()

def monitor_servers(app):
    """Background thread function to monitor servers."""
    with app.app_context():
        from .models import ServerStatus, Config  # Import models within the app context

        while True:
            servers = ServerStatus.query.all()
            config = Config.query.first()
            polling_period = config.polling_period if config else 300

            logging.info(f"Starting server check. Total servers to check: {len(servers)}")

            for server in servers:
                check_server_status(server)

            logging.info(f"Server check complete. Sleeping for {polling_period} seconds.")
            time.sleep(polling_period)  # Use the polling period from the database

def check_server_status(server):
    hostname_or_ip = server.ip_address
    tcp_status, udp_status = 'Down', 'Down'

    logging.info(f"Checking server: {server.name} ({hostname_or_ip})")

    try:
        resolved_ip = socket.gethostbyname(hostname_or_ip)
        logging.info(f"Resolved {hostname_or_ip} to {resolved_ip}")
    except socket.gaierror as e:
        logging.error(f"Failed to resolve {hostname_or_ip}: {str(e)}")
        resolved_ip = None

    if resolved_ip:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            try:
                sock.connect((resolved_ip, 16384))
                tcp_status = 'Up'
                logging.info(f"TCP check passed for {server.name}")
            except Exception as e:
                logging.warning(f"TCP check failed for {server.name}: {str(e)}")

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(1)
            try:
                sock.sendto(b"", (resolved_ip, 16384))
                udp_status = 'Up'
                logging.info(f"UDP check passed for {server.name}")
            except Exception as e:
                logging.warning(f"UDP check failed for {server.name}: {str(e)}")

        server.tcp_status = tcp_status
        server.udp_status = udp_status
        server.last_checked = datetime.datetime.now()

        db.session.commit()
        logging.info(f"Status for {server.name}: TCP={tcp_status}, UDP={udp_status}")
    else:
        logging.error(f"Skipping checks for {server.name} due to unresolved hostname.")

