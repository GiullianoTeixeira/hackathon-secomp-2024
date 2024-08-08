from flask import Flask, request, render_template, redirect, url_for
import tempfile
import os
import shutil

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Create a temporary directory for this request
            temp_dir = tempfile.mkdtemp()
            filename = file.filename
            filepath = os.path.join(temp_dir, filename)
            file.save(filepath)
            
            # Pass the temp_dir and filename to the template
            return redirect(url_for('index', filename=filename, temp_dir=temp_dir))
        else:
            return redirect(request.url)
    
    filename = request.args.get('filename')
    temp_dir = request.args.get('temp_dir')
    
    # Render the template with the filename and temp_dir
    if filename and temp_dir:
        filepath = os.path.join(temp_dir, filename)
        if os.path.exists(filepath):
            # Clean up the temporary directory after use
            os.remove(filepath)
            shutil.rmtree(temp_dir)
        return render_template('index.html', filename=filename, temp_dir=temp_dir)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
