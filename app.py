import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from htr import textRecog
 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./input/"
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    print('Route works')
    # return 'Coming soon'
    return render_template("upload.html")


@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            print("file uploaded")
            return show_result(filepath)


@app.route('/result', methods=['GET'])
def show_result(filepath):
    text = textRecog(filepath)
    # print(text)
    return render_template("result.html", text=text)

if __name__ == '__main__':
    app.debug = True
    app.run()