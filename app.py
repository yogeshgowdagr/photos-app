# Main Flask app entry point


from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify, send_file
import os
from werkzeug.utils import secure_filename

from config import PHOTO_FOLDER, THUMBNAIL_FOLDER, PHOTO_EXTENSIONS, VIDEO_EXTENSIONS, USERS
from utils.thumbnailer import generate_all_thumbnails

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this for production

def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in PHOTO_EXTENSIONS or ext in VIDEO_EXTENSIONS

def get_files():
    files = []
    for fname in os.listdir(PHOTO_FOLDER):
        if allowed_file(fname):
            ext = os.path.splitext(fname)[1].lower()
            files.append({
                'name': fname,
                'is_photo': ext in PHOTO_EXTENSIONS,
                'is_video': ext in VIDEO_EXTENSIONS,
                'thumbnail': f"/thumbnail/{fname}" if ext in PHOTO_EXTENSIONS else None
            })
    return files

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect(url_for('gallery'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/gallery')
def gallery():
    if 'user' not in session:
        return redirect(url_for('login'))
    files = get_files()
    return render_template('index.html', files=files, username=session['user'])

@app.route('/photo/<filename>')
def photo(filename):
    return send_from_directory(PHOTO_FOLDER, filename)

@app.route('/thumbnail/<filename>')
def thumbnail(filename):
    return send_from_directory(THUMBNAIL_FOLDER, filename)

@app.route('/video/<filename>')
def video(filename):
    return send_from_directory(PHOTO_FOLDER, filename)

@app.route('/download', methods=['POST'])
def download():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    files = request.form.getlist('files')
    import zipfile
    from io import BytesIO
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        for fname in files:
            fpath = os.path.join(PHOTO_FOLDER, fname)
            if os.path.exists(fpath):
                zipf.write(fpath, arcname=fname)
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='photos.zip')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    generate_all_thumbnails()
    app.run(host="0.0.0.0", port=5000)
