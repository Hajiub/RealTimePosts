from flask_caching import Cache
from flask_assets import Environment
from flask_debugtoolbar import DebugToolbarExtension

from flask_login import LoginManager
from app.models import User
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect


cache = Cache()

assets_env = Environment()

debug_toolbar = DebugToolbarExtension()



limiter = Limiter(get_remote_address)

csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)