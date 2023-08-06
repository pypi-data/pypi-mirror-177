"""
This module starts the backend of the web
"""
import os, sys, time, signal, traceback
from multiprocessing import Process
from importlib import import_module
from pathlib import Path

from flask import Flask, render_template, send_from_directory, request, jsonify
import webbrowser

from . import MACROS, Xponge, Model
from .commands import *

def open_webbrowser(url):
    time.sleep(0.5)
    webbrowser.open(url, 1)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def run():
    app = Flask(MACROS.PACKAGE,
                template_folder=os.path.join(os.path.dirname(__file__), "templates"),
                static_folder=os.path.join(os.path.dirname(__file__), "static"))

    app.template_filter('localization')(MACROS.localization)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(os.path.dirname(__file__), "static"),
                                   path='favicon.ico',
                                   mimetype='image/vnd.microsft.icon')

    @app.route('/')
    def index():
        return render_template("index.html", translation=render_template("translation.js"))

    @app.route("/cmd", methods=['POST'])
    def cmd():
        MACROS.CMD = None
        MACROS.TEXT = ""
        MACROS.TEMP = None
        value = request.form["value"]
        if not value:
            return jsonify({"text":""})
        try:
            try:
                exec(f"MACROS.TEMP = {value}", globals())
                if MACROS.TEMP is not None:
                    MACROS.TEXT += f"{MACROS.TEMP}"
            except SyntaxError:
                exec(value, globals())
            return jsonify({"text":MACROS.TEXT, "cmd":MACROS.CMD})
        except:
            return jsonify({"text":f"{traceback.format_exc()}"})

    @app.route("/exit", methods=["POST"])
    def exit():
        os.kill(os.getpid(), signal.SIGINT)
        return ""

    MACROS.APP = app
    Process(target=open_webbrowser, args=("http://127.0.0.1:10696",)).run()
    app.run(port=10696)