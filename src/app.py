import requests, os, subprocess
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from tools import dumpemail
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
        output+="<li><a href='analysis/"+f+"'>"+f+"</a></li>"
    output +="</ul>"
    return output

@app.route('/u', methods=['GET', 'POST'])
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
            filename = filename.lower()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            subprocess.call("msgconvert "+app.config['UPLOAD_FOLDER']+"/"+filename, shell=True)
            subprocess.call("mv *.eml uploads/",shell=True)
            subprocess.call("rm uploads/*.msg",shell=True)
            return redirect(url_for('upload_file',
                                    filename=filename))
    return render_template("upload.html",files=get_file_list())

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/analysis/<filename>')
def analysis(filename):
    headers_str = ""
    try:
        if('.eml' in filename.lower()):
            headers_str+=str(dumpemail(UPLOAD_FOLDER+'/'+filename))
        return render_template('analysis.html',filename=filename, headers=headers_str)
    except Exception as e:
        return(render_template('analysis.html',filename=filename,headers="Sorry, something's gone wrong!<br>"+str(e.with_traceback)))

@app.route('/')
def index():
    return render_template("index.html",files=get_file_list())