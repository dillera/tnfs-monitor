from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import db, ServerStatus, Config 
import socket
import subprocess
import logging



main_bp = Blueprint('main', __name__)

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("add_server.log"),
                              logging.StreamHandler()])



@main_bp.route('/')
def view_servers():
    servers = ServerStatus.query.all()
    config = Config.query.first()
    polling_period = config.polling_period if config else 300

    return render_template('view_servers.html', servers=servers, polling_period=polling_period)
    
###############

@main_bp.route('/adminpokey')
def admin():
    servers = ServerStatus.query.all()
    config = Config.query.first()

    # If there is no Config in the database, set a default value
    if not config:
        config = Config(polling_period=300)  # Default value

    return render_template('admin.html', servers=servers, config=config)

###############

def is_valid_hostname_or_ip(hostname_or_ip):
    """Check if the given hostname or IP is valid and reachable."""
    try:
        # Try to resolve the hostname/IP address
        resolved_ip = socket.gethostbyname(hostname_or_ip)
        logging.info(f'Successfully resolved {hostname_or_ip} to {resolved_ip}')
        
        # Ping the IP address to check if it's reachable
        result = subprocess.run(['ping', '-c', '1', resolved_ip], stdout=subprocess.PIPE)
        
        # If ping returns a 0 return code, the host is reachable
        if result.returncode == 0:
            logging.info(f'Ping to {resolved_ip} successful')
            return True
        else:
            logging.warning(f'Ping to {resolved_ip} failed')
            return False
    except socket.gaierror as e:
        # If resolution fails, it's not a valid hostname/IP
        logging.error(f'Failed to resolve {hostname_or_ip}: {str(e)}')
        return False

@main_bp.route('/add', methods=['GET', 'POST'])
def add_server():
    if request.method == 'POST':
        name = request.form['name']
        hostname_or_ip = request.form['hostname_or_ip']

        logging.info(f'Attempting to add server: Name={name}, Hostname/IP={hostname_or_ip}')

        if not name or not hostname_or_ip:
            flash('Both Server Name and Hostname or IP Address are required!', 'error')
            return redirect(url_for('main.add_server'))

        if not is_valid_hostname_or_ip(hostname_or_ip):
            flash(f'Error: {hostname_or_ip} is not a valid or reachable hostname/IP address!', 'error')
            return redirect(url_for('main.add_server'))

        server = ServerStatus(name=name, ip_address=hostname_or_ip)
        db.session.add(server)
        db.session.commit()

        flash(f'Server {name} ({hostname_or_ip}) added successfully and is reachable!', 'success')
        return redirect(url_for('main.admin'))

    return render_template('add_server.html')

###############

@main_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_server(id):
    server = ServerStatus.query.get(id)
    if request.method == 'POST':
        server.name = request.form['name']
        server.ip_address = request.form['hostname_or_ip']
        db.session.commit()
        flash(f'Server {server.name} updated successfully!', 'success')
        return redirect(url_for('main.admin'))
    return render_template('edit_server.html', server=server)

###############

@main_bp.route('/delete/<int:id>')
def delete_server(id):
    server = ServerStatus.query.get(id)
    db.session.delete(server)
    db.session.commit()
    flash(f'Server {server.name} deleted successfully!', 'success')
    return redirect(url_for('main.admin'))


###############

@main_bp.route('/update_polling_period', methods=['POST'])
def update_polling_period():
    polling_period = int(request.form['polling_period'])
    config = Config.query.first()

    if config:
        config.polling_period = polling_period
    else:
        config = Config(polling_period=polling_period)
        db.session.add(config)
    
    db.session.commit()
    flash(f'Polling period updated to {polling_period} seconds.', 'success')
    return redirect(url_for('main.admin'))

    
