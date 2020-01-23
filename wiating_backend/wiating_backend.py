# -*- coding: utf-8 -*-

"""Python Flask Wiating API backend
"""
import flask_monitoringdashboard as dashboard
from os import environ as env
from werkzeug.exceptions import HTTPException

from flask import Flask, jsonify, redirect, render_template, request
from flask_cors import CORS

from . import constants
from .config import DefaultConfig
from .image import images
from .points import points



def configure_blueprints(app):
    """Configure blueprints in views."""

    with app.app_context():
        for bp in [images, points]:
            app.register_blueprint(bp)


def configure_dashboard(app):
    def group_by_user_sub():
        return hash(request.headers.get("Authorization", None))

    dashboard.config.group_by = group_by_user_sub
    dashboard.config.init_from(file=env.get(constants.DASHBOARD_CONFIG_FILE_PATH))
    dashboard.bind(app)


def configure_app(app, config):
    app.config.from_object(config)


def configure_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_auth_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
        return response


def configure_home(app):
    @app.route('/')
    def home():
        return render_template('home.html')


def create_app(config=DefaultConfig()):
    app = Flask(__name__, static_url_path='/public', static_folder='./public')
    configure_app(app, config)
    configure_blueprints(app)
    configure_dashboard(app)
    configure_home(app)

    CORS(app)
    return app
