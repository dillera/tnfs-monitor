from . import db

class ServerStatus(db.Model):
    __tablename__ = 'server_status'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(100), nullable=False)
    last_checked = db.Column(db.DateTime, nullable=True)
    tcp_status = db.Column(db.String(10), nullable=True)
    udp_status = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f'<ServerStatus {self.name}>'

class Config(db.Model):
    __tablename__ = 'config'

    id = db.Column(db.Integer, primary_key=True)
    polling_period = db.Column(db.Integer, nullable=False, default=300)  # Default polling period is 300 seconds

    def __repr__(self):
        return f'<Config polling_period={self.polling_period}>'

