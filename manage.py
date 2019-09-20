from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

from datetime import datetime
from . import login_manager


if __name__ == '__main__':
    manager.run()