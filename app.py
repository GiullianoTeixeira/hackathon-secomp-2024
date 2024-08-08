from flask import Flask, request, render_template, jsonify
import os
import tempfile
import json

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
           
@app.route('/index', methods=['GET'])
def index_html():
    return render_template('index.html')

@app.route('/insert_info_pt', methods=['GET'])
def info_pt():
    return render_template('insert_info_pt.html')

@app.route('/insert_info_en', methods=['GET'])
def info_en():
    return render_template('insert_info_en.html')

@app.route('/results_pt', methods=['GET'])
def results_pt():
    return render_template('results_pt.html')

@app.route('/results_en', methods=['GET'])
def results_en():
    return render_template('results_en.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    form_data = {}
    image_urls = {}

    if request.method == 'POST':
        # Creating a temporary directory for this request
        temp_dir = tempfile.mkdtemp()

        # Handling text data
        form_data['machine_name'] = request.form.get('machineName')
        form_data['machine_type'] = request.form.get('machineType')

        # Handling image uploads
        for key in request.files:
            file = request.files[key]
            if file and allowed_file(file.filename):
                filename = file.filename
                filepath = os.path.join(temp_dir, filename)
                file.save(filepath)
                image_urls[key] = filename  # Storing image filenames

        json_data = {
            'form_data': form_data,
            'image_urls': image_urls
        }
        
        with open('user_info.json', 'w') as json_file:
            json.dump(json_data, json_file)

        return jsonify(json_data)

    return render_template('index.html')

@app.route('/data_pt', methods=['GET'])
def get_data_pt(json_data):
    data = chatGPT_response_PT(json_data)
    return jsonify(data)


@app.route('/data_en', methods=['GET'])
def get_data_en(json_data):
    data = chatGPT_response_EN(json_data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
