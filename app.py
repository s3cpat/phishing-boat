import requests, os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['eml','msg', 'txt'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_list():
    uploads = os.listdir(UPLOAD_FOLDER)
    output = "<ul>"
    for f in uploads:
        output+="<li><a href='uploads/"+f+"'>"+f+"</a></li>"
    output +="</ul>"
    return output

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Phishing Boat</title>
    <h1>Phishing Boat</h1>
    <h2>Upload an email for analysis</h2>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file><i style="color:red">Allowed types: .eml, .msg, .txt</i><br>
      <input type=submit value=Upload>
    </form>
    <br><h2>Files</h2><br>
    '''+get_file_list()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
