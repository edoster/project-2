"""
John Doe's Flask API.
"""

"""
Configuration Logic
"""
import os
import configparser

def parse_config(config_paths):
    config_path = None
    for f in config_paths:
        if os.path.isfile(f):
            config_path = f
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

config = parse_config(["credentials.ini", "default.ini"])
port = config["SERVER"]["PORT"]
debug = config["SERVER"]["DEBUG"]


from flask import Flask, abort, send_from_directory, render_template

app = Flask(__name__)

@app.route("/<path:filename>")
def pageErrors(filename):
    # If we have any illegal characters, we will abort with 403
    if '..' in filename or '~' in filename:
        abort(403)
    try:
    
    # Otherwise, transmit the file with the status 200
        return send_from_directory('pages/', filename), 200
    
    # If we do not have a page then throw the error code
    except FileNotFoundError:
        abort(404)


@app.errorhandler(403)
def forbidden(e):
    return send_from_directory('pages/', '403.html'), 403

@app.errorhandler(404)
def notFound(e):
    return send_from_directory('pages', '404.html'), 404


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=port)
