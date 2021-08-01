import os
from multiprocessing import Process
from flask import Flask, render_template, request, redirect
from flask.helpers import flash
from test import parallel_task
from werkzeug.utils import secure_filename
from constants import UPLOAD_FOLDER


app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template("main.html")


@app.route('/instagram', methods=['POST', 'GET'])
def instagram():
    if request.method == "GET":
        return render_template("instagram.html")
    if request.method == "POST":

        # Get the required args
        username = request.form.get('username')
        password = request.form.get('password')
        caption = request.form.get('caption')
        file = request.files.get("file")

        if file.getbuffer().nbytes == 0:
            flash("Instagram posts requires an image", 'error')
            return redirect('/instagram')
        
        filename = secure_filename(file.name)

        # Run the selenium in a separate thread
        execute_parallel(parallel_task, (username, password, caption, filename, file))
        return redirect('/instagram')


@app.route('/telegram', methods=['POST', 'GET'])
def telegram():
    if request.method == "GET":
        return render_template("telegram.html")
    if request.method == "POST":

        # Get the required args
        api_token = request.form.get('api_token')
        group_id = request.form.get('group_id')
        message = request.form.get('message')

        # Run the selenium in a separate thread
        execute_parallel(parallel_task, (api_token, group_id, message))
        return redirect('/telegram')


def execute_parallel(function, args):
    p = Process(target=function, args=args)
    p.daemon = True
    p.run()


if __name__ == "__main__":
    app.run(debug=True)
