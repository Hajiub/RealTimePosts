from flask import Flask, current_app, render_template
from webassets.loaders import PythonLoader
from app import assets
from flask_migrate import Migrate
from app.extensions import (
    cache,
    assets_env,
    debug_toolbar, 
    login_manager,
    limiter,
    csrf
)
from app.models import db


def create_app(object_name):
    """ 
    Arguments:
        ojbect_name: the pythong path of the config object,
                    e.g. app.settings.ProdConfig
    """
    

    app = Flask(__name__)
    app.config.from_object(obj=object_name)
    # Initialize the cache
    cache.init_app(app)

    # Initialize the debug toolbar
    debug_toolbar.init_app(app)
    
    # Initialize SQLAlchemy
    db.init_app(app)

    migrate = Migrate(app, db)

    limiter.init_app(app)

    login_manager.init_app(app)

    csrf.init_app(app)

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)
    
    # Register blueprints    
    from app.controllers.main import main as main_bp
    from app.post.routes import blog_post as post_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(post_bp)
    
    return app