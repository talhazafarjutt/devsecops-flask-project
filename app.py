#!/usr/bin/env python3
import os
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask import Flask, render_template, render_template_string, request, redirect
from db_seed import setup_db
from routes import init

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret-key-for-dev-only")
app.config["BOOTSTRAP_SERVE_LOCAL"] = True
app.config["CKEDITOR_SERVE_LOCAL"] = True
# Disable debug mode in production
app.config["DEBUG"] = False
bootstrap = Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
ckeditor = CKEditor()

ckeditor.init_app(app)
init()
setup_db()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")


@app.errorhandler(404)
def page_not_found(error):
    # Don't expose detailed error information in production
    return render_template("404.html"), 404
