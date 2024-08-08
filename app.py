from flask import Flask, request, render_template, jsonify
import os
import tempfile
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    form_data = {}
    image_urls = {}

    if request.method == 'POST':
        # Create a temporary directory for this request
        temp_dir = tempfile.mkdtemp()

        # Handle text data
        form_data['nome_maquina'] = request.form.get('nomeMaquina')
        form_data['tipo_maquina'] = request.form.get('tipoMaquina')

        # Handle image uploads
        for key in request.files:
            file = request.files[key]
            if file and allowed_file(file.filename):
                filename = file.filename
                filepath = os.path.join(temp_dir, filename)
                file.save(filepath)
                image_urls[key] = filename  # Store image filenames

        json_data = {
            'form_data': form_data,
            'image_urls': image_urls
        }
        
        with open('data.json', 'w') as json_file:
            json.dump(json_data, json_file)

        return jsonify(json_data)

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='127.0.0.1', port=5000)
